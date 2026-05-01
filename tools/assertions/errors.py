import allure

from clients.http.error_schema import ValidationErrorSchema, ValidationErrorResponseSchema, InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.logger import get_logger

logger = get_logger("ERRORS_ASSERTIONS")

@allure.step("Check validation error")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    Args:
        actual: Фактическая ошибка.
        expected: Ожидаемая ошибка.

    Raises:
        AssertionError: Если значения полей не совпадают.

    """
    logger.info("Check validation error")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")


@allure.step("Check validation error response")
def assert_validation_error_response(
        actual: ValidationErrorResponseSchema,
        expected: ValidationErrorResponseSchema
):
    """Проверяет, что объект ответа API с ошибками валидации (`ValidationErrorResponseSchema`)
    соответствует ожидаемому значению.

    Args:
        actual: Фактический ответ API.
        expected: Ожидаемый ответ API.

    Raises:
        AssertionError: Если значения полей не совпадают.

    """
    logger.info("Check validation error response")
    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)


@allure.step("Check internal error response")
def assert_internal_error_response(
        actual: InternalErrorResponseSchema,
        expected: InternalErrorResponseSchema
):
    """Функция для проверки внутренней ошибки. Например, ошибки 404 (File not found).

    Args:
        actual: Фактический ответ API.
        expected: Ожидаемый ответ API.

    Raises:
        AssertionError: Если значения полей не совпадают.

    """
    logger.info("Check internal error response")
    assert_equal(actual.details, expected.details, "details")