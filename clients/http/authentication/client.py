import allure
from requests import Response

from clients.http.authentication.schema import LoginRequestSchema, RefreshRequestSchema, LoginResponseSchema
from clients.http.client import HTTPClient
from clients.http.public_builder import get_public_http_client
from tools.http.enums import HTTPRoutes


class AuthenticationClient:
    """
    Клиент для работы с /api/v1/authentication
    """
    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Authenticate user")
    def login_api(self, request: LoginRequestSchema) -> Response:
        """Метод выполняет аутентификацию пользователя.

        Args:
            request: Объект вида LoginRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.post(f'{HTTPRoutes.AUTHENTICATION}/login', json=request.model_dump())

    @allure.step("Refresh authentication token")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """Метод обновляет токен авторизации.

        Args:
            request: Объект вида RefreshRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response

        """
        return self._client.post(f'{HTTPRoutes.AUTHENTICATION}/refresh', json=request.model_dump())

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """Высокоуровневый метод, выполняющий аутентификацию пользователя.

        Args:
            request: Объект вида LoginRequestSchema.

        Returns:
            LoginResponseSchema: Ответ от сервера в виде объекта LoginResponseSchema.

        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    Returns:
        AuthenticationClient: Готовый к использованию AuthenticationClient.

    """
    return AuthenticationClient(client=get_public_http_client())
