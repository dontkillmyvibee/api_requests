import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.courses.schema import GetCoursesQuerySchema, CreateCourseRequestSchema, UpdateCourseRequestSchema, \
    CreateCourseResponseSchema
from clients.http.private_builder import get_private_http_client, AuthenticationUserSchema
from tools.http.enums import HTTPRoutes


class CoursesClient:
    """
    Клиент для работы с /api/v1/courses
    """
    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Get courses")
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """Метод получения списка курсов.


        Args:
            query: Объект типа GetCoursesQuerySchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response

        """
        return self._client.get(f"{HTTPRoutes.COURSES}", params=query.model_dump(by_alias=True))

    @allure.step("Get course by id {course_id}")
    def get_course_api(self, course_id: str) -> Response:
        """Метод получения курса.

        Args:
            course_id: Идентификатор курса.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response

        """
        return self._client.get(f"{HTTPRoutes.COURSES}/{course_id}")

    @allure.step("Create course")
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """Метод создания курса.

        Args:
            request: Объект типа CreateCourseRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response
        """
        return self._client.post(f"{HTTPRoutes.COURSES}", json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """Метод обновления курса.

        Args:
            course_id: Идентификатор курса.
            request: Объект типа UpdateCourseRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response
        """
        return self._client.patch(f"{HTTPRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete course by id {course_id}")
    def delete_course_api(self, course_id: str) -> Response:
        """Метод удаления курса.

        Args:
            course_id: Идентификатор курса.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response
        """
        return self._client.delete(f"{HTTPRoutes.COURSES}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """Функция создает экземпляр CoursesClient с уже настроенным HTTP-клиентом

    Args:
        user: Объект типа AuthenticationUserSchema.

    Returns:
        CoursesClient: Готовый к использованию CoursesClient.

    """
    return CoursesClient(client=get_private_http_client(user))
