import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.exercises.schema import GetExercisesQuerySchema, GetExerciseResponseSchema, \
    CreateExerciseRequestSchema, UpdateExerciseRequestSchema, GetExercisesResponseSchema, CreateExerciseResponseSchema, \
    UpdateExerciseResponseSchema
from clients.http.private_builder import AuthenticationUserSchema, get_private_http_client
from tools.http.enums import HTTPRoutes


class ExercisesClient:
    """
    Клиент для работы с /api/v1/exercises
    """

    def __init__(self, client: HTTPClient):
        self._client = client

    @allure.step("Get exercises")
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """

        Args:
            query:

        Returns:

        """
        return self._client.get(f"{HTTPRoutes.EXERCISES}", params=query.model_dump(by_alias=True))

    @allure.step("Get exercise with id: {exercise_id}")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """Метод получения задания.

        Args:
            exercise_id: Идентификатор задания.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.get(f"{HTTPRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """Метод получения списка заданий.

        Args:
            request: Объект типа CreateExerciseRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.post(f"{HTTPRoutes.EXERCISES}", json=request.model_dump(by_alias=True))

    @allure.step("Update exercise with id: {exercise_id}")
    def update_exercise_api(self, request: UpdateExerciseRequestSchema, exercise_id: str) -> Response:
        """Метод обновления задания.

        Args:
            request: Объект типа UpdateExerciseRequestSchema.
            exercise_id: Идентификатор задания.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.patch(f"{HTTPRoutes.EXERCISES}/{exercise_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete exercise with id: {exercise_id}")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Метод удаления задания.

        Args:
            exercise_id: Идентификатор задания.

        Returns:
            Response: Ответ от сервера в виде объекта requests.Response.

        """
        return self._client.delete(f"{HTTPRoutes.EXERCISES}/{exercise_id}")

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(
            self,
            exercise_id: str,
            request: UpdateExerciseRequestSchema
    ) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id=exercise_id, request=request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """Функция создает экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    Args:
        user: Объект типа AuthenticationUserSchema.

    Returns:
        ExercisesClient: Готовый к использованию ExercisesClient.

    """
    return ExercisesClient(client=get_private_http_client(user))
