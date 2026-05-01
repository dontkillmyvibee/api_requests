from functools import lru_cache

from clients.http.builder import build_http_client
from clients.http.client import HTTPClient
from pydantic import BaseModel

from clients.http.authentication.client import get_authentication_client
from clients.http.authentication.schema import LoginRequestSchema
from config import settings


class AuthenticationUserSchema(BaseModel, frozen=True):
    email: str
    password: str


@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> HTTPClient:
    """Создает экземпляр HTTPClient.

        Формирует экземпляр HTTPClient с использованием метода clients.http.builder.build_http_client, передает в клиент
        аргументы согласно методу build_http_client, расширяя его авторизационным токеном.
        timeout и base_url берется из env файла.

    Args:
        user (AuthenticationUserSchema): Объект типа AuthenticationUserSchema

    Returns:
        HTTPClient: Настроенный экземпляр HTTPClient, готовый к использованию в HTTP клиентах требующих авторизованного
        пользователя.

    """
    authentication_client = get_authentication_client()

    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)

    return build_http_client(
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"}
    )
