from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.http.authentication.client import AuthenticationClient
from clients.http.authentication.schema import LoginRequestSchema, LoginResponseSchema
from clients.http.error_schema import InternalErrorResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response, assert_login_with_invalid_email_and_password
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    @allure.title("Login with correct email and password")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        request = LoginRequestSchema(email=function_user.email, password=function_user.password)
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Login with invalid email and password")
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    def test_login_with_invalid_email_and_password(self, authentication_client: AuthenticationClient):
        request = LoginRequestSchema(email=fake.email(domain="mail.ru"), password=fake.password())
        response = authentication_client.login_api(request)

        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_login_with_invalid_email_and_password(response_data)