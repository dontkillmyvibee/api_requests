from clients.http.builder import build_http_client
from clients.http.client import HTTPClient
from config import settings


def get_public_http_client() -> HTTPClient:
    """Создает экземпляр HTTPClient.

    Формирует экземпляр HTTPClient с использованием метода clients.http.builder.build_http_client, передает в клиент
        аргументы согласно методу build_http_client, не расширяя его дополнительными заголовками для имитации
        неавторизованного пользователя.
        timeout и base_url берется из env файла.

    Returns:
        HTTPClient: HTTPClient: Настроенный экземпляр HTTPClient, готовый к использованию в HTTP клиентах требующих
        неавторизованного пользователя.

    """
    return build_http_client(
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout,
    )
