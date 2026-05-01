import allure

from clients.http.users.schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema, \
    GetUserResponseSchema
from tools.assertions.base import assert_equal

from tools.logger import get_logger

logger = get_logger("USER_ASSERTIONS")


@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """Проверяет, что ответ на создание пользователя соответствует запросу.

    Args:
        request: Исходный запрос на создание пользователя.
        response: Ответ API с данными пользователя.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check create user response")
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")


@allure.step("Check user")
def assert_user(actual: UserSchema, expected: UserSchema):
    """Проверяет, что фактические данные пользователя соответствуют ожидаемым.

    Args:
        actual: Фактические данные пользователя.
        expected: Ожидаемые данные пользователя.

    Returns:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check user")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")
    assert_equal(actual.id, expected.id, "id")


@allure.step("Check get user response")
def assert_get_user_response(
        get_user_response: GetUserResponseSchema,
        create_user_response: CreateUserResponseSchema
):
    """Проверяет, что ответ на получение пользователя соответствует ответу на его создание.

    Args:
        get_user_response: Ответ API при запросе данных пользователя.
        create_user_response: Ответ API при создании пользователя.

    Raises:
        AssertionError: Если данные пользователя не совпадают.

    """
    logger.info("Check get user response")
    assert_user(get_user_response.user, create_user_response.user)