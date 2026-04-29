import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.files.schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.http.private_builder import AuthenticationUserSchema, get_private_http_client
from tools.http.enums import HTTPRoutes


class FilesClient:
    """
    Клиент для работы с /api/v1/files
    """
    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Get file by id {file_id}")
    def get_file_api(self, file_id: str) -> Response:
        """Метод получения файла.

        Args:
            file_id: Идентификатор файла.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.get(f"{HTTPRoutes.FILES}/{file_id}")

    @allure.step("Delete file by id {file_id}")
    def delete_file_api(self, file_id: str) -> Response:
        """Метод удаления файла.

        Args:
            file_id: Идентификатор файла

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.delete(f"{HTTPRoutes.FILES}/{file_id}")

    @allure.step("Create file")
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        """Метод создания файла.

        Args:
            request: Объект типа CreateFileRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.post(
            HTTPRoutes.FILES,
            data=request.model_dump(by_alias=True, exclude={'upload_file'}),
            files={"upload_file": request.upload_file.read_bytes()}
        )

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)


def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """Функция создает экземпляр FilesClient с уже настроенным HTTP-клиентом.

    Args:
        user: Объект типа AuthenticationUserSchema.

    Returns:
        FilesClient: Готовый к использованию FilesClient.

    """
    return FilesClient(client=get_private_http_client(user))
