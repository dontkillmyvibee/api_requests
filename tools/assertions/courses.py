import allure

from clients.http.courses.schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, CourseSchema, \
    GetCoursesResponseSchema, CreateCourseResponseSchema, CreateCourseRequestSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user
from tools.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")

@allure.step("Check update course response")
def assert_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema
):
    """Проверяет, что ответ API при обновлении курса содержит ожидаемые данные.

    Args:
        request: Запрос на обновление курса.
        response: Ответ API на обновление курса.

    Raises:
        AssertionError: Если данные не соответствуют ожидаемым.

    """
    logger.info("Check update course response")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check course")
def assert_course(actual: CourseSchema, expected: CourseSchema):
    """Проверяет, что фактические данные курса соответствуют ожидаемым.

    Args:
        actual: Фактические данные курса.
        expected: Ожидаемые данные курса.

    Raises:
        AssertionError: Если данные не соответствуют ожидаемым.

    """
    logger.info("Check course")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


@allure.step("Check get courses response")
def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_courses_response: list[CreateCourseResponseSchema]
):
    logger.info("Check get courses response")
    assert_length(get_courses_response.courses, create_courses_response, "courses")

    for index, create_courses_response in enumerate(create_courses_response):
        assert_course(get_courses_response.courses[index], create_courses_response.course)


@allure.step("Check create course response")
def assert_create_course_response(
        request: CreateCourseRequestSchema,
        response: CreateCourseResponseSchema
):
    """Проверяет, что данные ответа на создание курса соответствуют запросу.

    Args:
        request: Запрос на создание курса.
        response: Ответ API с созданным курсом.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает с запросом.

    """
    course = response.course

    logger.info("Check create course response")
    assert_equal(course.title, request.title, "title")
    assert_equal(course.max_score, request.max_score, "max_score")
    assert_equal(course.min_score, request.min_score, "min_score")
    assert_equal(course.description, request.description, "description")
    assert_equal(course.estimated_time, request.estimated_time, "estimated_time")

    assert_equal(course.preview_file.id, request.preview_file_id, "preview_file_id")
    assert_equal(course.created_by_user.id, request.created_by_user_id, "created_by_user_id")