from http import HTTPMethod
from typing import Any

from requests import Session, Response


class HTTPClient:
    """Базовый HTTP-клиент для работы с API(надстройка над requests).

    Использует объект Session для выполнения HTTP-запросов с заданным таймаутом и базовым URL.
    """

    def __init__(self, client: Session, base_url: str, timeout: int):
        self.__client = client
        self.__base_url = base_url
        self.__timeout = timeout

    def __request(self, method: str, url: str, **kwargs) -> Response:
        """Внутренний метод для отправки HTTP-запроса.

                Формирует полный URL, объединяя базовый URL и путь, и отправляет запрос
                с использованием объекта requests.Session.

                Args:
                    method (str): HTTP-метод (например, «GET», «POST»).
                    url (str): Путь к ресурсу (например, «users/1»).
                    **kwargs: Дополнительные аргументы для метода request (params, json, data и т. д.).

                Returns:
                    Response: Объект Response с результатом запроса.
                """
        full_url = f"{self.__base_url}/{url}"
        return self.__client.request(method=method, url=full_url, timeout=self.__timeout, **kwargs)

    def get(self, url: str, params: Any | None = None) -> Response:
        """Метод для отправки GET-запроса к ресурсу.

        Args:
            url (str): Путь к ресурсу.
            params (Any | None): Параметры запроса, которые будут добавлены в URL как query-параметры.

        Returns:
            Response: Объект Response с результатом GET-запроса.
        """
        return self.__request(method=HTTPMethod.GET, url=url, params=params)

    def post(self, url: str, json: Any | None = None, data: Any | None = None, files: str | None = None) -> Response:
        """Метод для отправки POST-запроса к ресурсу.

        Args:
            url (str): Путь к ресурсу.
            json (Any | None): Данные в формате JSON для тела запроса.
            data (Any | None): Данные для тела запроса в необработанном виде.
            files (str | None): Файлы для отправки.

        Returns:
            Response: Объект Response с результатом POST-запроса.
        """
        return self.__request(method=HTTPMethod.POST, url=url, json=json, data=data, files=files)

    def patch(self, url: str, json: Any | None = None) -> Response:
        """Метод для отправки PATCH-запроса для частичного обновления ресурса.

        Args:
            url (str): Путь к ресурсу.
            json (Any | None): Данные в формате JSON для частичного обновления.

        Returns:
            Response: Объект Response с результатом PATCH-запроса.
        """
        return self.__request(method=HTTPMethod.PATCH, url=url, json=json)

    def delete(self, url: str) -> Response:
        """Метод для отправки DELETE-запрос для удаления ресурса.

        Args:
            url (str): Путь к ресурсу.

        Returns:
            Response: Объект Response с результатом DELETE-запроса.
        """

        return self.__request(method=HTTPMethod.DELETE, url=url)
