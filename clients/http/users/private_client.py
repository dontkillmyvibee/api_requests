import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.private_builder import AuthenticationUserSchema, get_private_http_client
from clients.http.users.schema import UpdateUserRequestSchema, GetUserResponseSchema
from tools.http.enums import HTTPRoutes


class PrivateUsersClient:
    """
    Клиент для работы с /api/v1/users
    """
    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Get user me")
    def get_user_me_api(self) -> Response:
        """Метод получения текущего пользователя

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.get(f"{HTTPRoutes.USERS}/me")

    @allure.step("Get user by id {user_id}")
    def get_user_api(self, user_id: str) -> Response:
        """Метод получения пользователя по идентификатору.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.get(f"{HTTPRoutes.USERS}/{user_id}")

    @allure.step("Update user by id {user_id}")
    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        """Метод обновления пользователя по идентификатору.

        Args:
            user_id: Идентификатор пользователя.
            request: Объект типа UpdateUserRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.patch(f"{HTTPRoutes.USERS}/{user_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete user by id {user_id}")
    def delete_user_api(self, user_id: str) -> Response:
        """Метод удаления пользователя по идентификатору.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.delete(f"{HTTPRoutes.USERS}/{user_id}")

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)


def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """Функция создает экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.

    Args:
        user: Объект типа AuthenticationUserSchema.

    Returns:
        PrivateUsersClient: Готовый к использованию PrivateUsersClient.

    """
    return PrivateUsersClient(client=get_private_http_client(user))
