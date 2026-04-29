import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.public_builder import get_public_http_client
from clients.http.users.schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.http.enums import HTTPRoutes


class PublicUsersClient:
    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Create user")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """Метод создания пользователя.

        Args:
            request: Объект типа CreateUserRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.post(HTTPRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    """Функция создает экземпляр PublicUsersClient с уже настроенным HTTP_клиентом.

    Returns:
        PublicUsersClient: Готовый к использованию PublicUsersClient.

    """
    return PublicUsersClient(client=get_public_http_client())
