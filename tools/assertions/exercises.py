import allure

from clients.http.error_schema import InternalErrorResponseSchema
from clients.http.exercises.schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, ExerciseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response
from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")


@allure.step("Check create exercise response")
def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """Проверяет, что данные ответа на создание задания соответствуют запросу.

    Args:
        request: Запрос на создание задания.
        response: Ответ API с созданным заданием.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает с запросом.

    """
    logger.info("Check create exercise response")
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """Проверяет, что фактические данные задания соответствуют ожидаемым.

    Args:
        actual: Фактические данные задания.
        expected: Ожидаемые данные задания.

    Raises:
        AssertionError: Если данные не соответствуют ожидаемым.

    """
    logger.info("Check exercise")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


@allure.step("Check get exercise response")
def assert_get_exercise_response(
        actual: GetExerciseResponseSchema,
        expected: CreateExerciseResponseSchema
):
    """Проверяет, что ответ API на получение задания совпадает с данными ранее созданного задания.

    Args:
        actual: Ответ API при запросе задания.
        expected: Ответ API, возвращённый при создании задания.

    Raises:
        AssertionError: Если данные задания не совпадают.

    """
    logger.info("Check get exercise response")
    assert_exercise(actual.exercise, expected.exercise)


@allure.step("Check update exercise response")
def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """Проверяет, что ответ API при обновлении задания содержит ожидаемые данные.

    Args:
        request: Запрос на обновление задания.
        response: Ответ API на обновление задания.

    Raises:
        AssertionError: Если данные не соответствуют ожидаемым.

    """
    logger.info("Check update exercise response")
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """Проверяет, что ответ API содержит ошибку 'Exercise not found'.

    Args:
        actual: Фактический ответ API после попытки получить удалённое задание.

    Raises:
        AssertionError: Если текст ошибки не соответствует ожидаемому.

    """
    logger.info("Check exercise not found response")
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)


@allure.step("Check get exercises response")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        created_exercises: list[CreateExerciseResponseSchema]
):
    """Проверяет, что ответ API на получение списка заданий содержит все ранее созданные задания
    и что данные каждого задания совпадают.

    Args:
        get_exercises_response: Ответ API при запросе списка заданий.
        created_exercises: Список ответов API, возвращённых при создании заданий.

    Raises:
        AssertionError: Если количество или данные заданий не совпадают.

    """
    logger.info("Check get exercises response")
    assert_length(get_exercises_response.exercises, created_exercises, "exercises")

    for index, created_exercise_response in enumerate(created_exercises):
        assert_exercise(
            get_exercises_response.exercises[index],
            created_exercise_response.exercise
        )
