import allure

from clients.http.authentication.schema import LoginResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")


@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    """Проверяет корректность ответа при успешной авторизации.

    Args:
        response: Объект типа LoginResponseSchema.

    Raises:
        AssertionError: Если какое-либо из условий не выполняется.

    """
    logger.info("Check login response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")