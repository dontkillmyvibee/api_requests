import allure

from clients.http.error_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema
from clients.http.files.schema import CreateFileRequestSchema, CreateFileResponseSchema, FileSchema, \
    GetFileResponseSchema
from config import settings
from tools.assertions.base import assert_equal
from tools.assertions.errors import assert_validation_error_response, assert_internal_error_response
from tools.logger import get_logger

logger = get_logger("FILES_ASSERTIONS")


@allure.step("Check create file response")
def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    """Проверяет, что ответ на создание файла соответствует запросу.

    Args:
        request: Исходный запрос на создание файла.
        response: Ответ API с данными файла.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check create file response")

    expected_url = f"{settings.http_client.client_url}static/{request.directory}/{request.filename}"

    assert_equal(str(response.file.url), expected_url, "url")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")


@allure.step("Check file")
def assert_file(actual: FileSchema, expected: FileSchema):
    """Проверяет, что фактические данные файла соответствуют ожидаемым.

    Args:
        actual: Фактические данные файла.
        expected: Ожидаемые данные файла.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check file")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.url, expected.url, "url")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.directory, expected.directory, "directory")


@allure.step("Check get file response")
def assert_get_file_response(
        get_file_response: GetFileResponseSchema,
        create_file_response: CreateFileResponseSchema
):
    """Проверяет, что ответ на получение файла соответствует ответу на его создание.

    Args:
        get_file_response: Ответ API при запросе данных файла.
        create_file_response: Ответ API при создании файла.

    Raises:
        AssertionError: Если данные файла не совпадают.

    """
    logger.info("Check get file response")
    assert_file(get_file_response.file, create_file_response.file)


@allure.step("Check create file with empty filename response")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    """Проверяет, что ответ на создание файла с пустым именем файла соответствует ожидаемой валидационной ошибке.

    Args:
        actual: Ответ от API с ошибкой валидации, который необходимо проверить.

    Raises:
        AssertionError: Если фактический ответ не соответствует ожидаемому.

    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "filename"]
            )
        ]
    )
    logger.info("Check create file with empty filename response")
    assert_validation_error_response(actual, expected)


@allure.step("Check create file with empty directory response")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    """Проверяет, что ответ на создание файла с пустым значением директории соответствует ожидаемой валидационной ошибке.

    Args:
        actual: Ответ от API с ошибкой валидации, который необходимо проверить.

    Raises:
        AssertionError: Если фактический ответ не соответствует ожидаемому.

    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "directory"]
            )
        ]
    )
    logger.info("Check create file with empty directory response")
    assert_validation_error_response(actual, expected)


@allure.step("Check file not found response")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    expected = InternalErrorResponseSchema(details="File not found")
    logger.info("Check file not found response")
    assert_internal_error_response(actual, expected)


@allure.step("Check get file with incorrect file id response")
def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    """Проверяет, что ответ API при запросе файла с некорректным идентификатором содержит ожидаемую ошибку валидации.

    Args:
        actual: Фактический ответ API с ошибкой валидации.

    Raises:
        AssertionError: Если структура или содержание ошибки не соответствуют ожиданию.

    """
    invalid_uuid_message = (
        "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` "
        "followed by [0-9a-fA-F-], found `i` at 1"
    )
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-file-id",
                context={"error": "invalid character: expected an optional prefix of `urn:uuid:` "
                                  "followed by [0-9a-fA-F-], found `i` at 1"},
                message=invalid_uuid_message,
                location=["path", "file_id"]
            )
        ]
    )
    logger.info("Check get file with incorrect file id response")
    assert_validation_error_response(actual, expected)