import pytest

from clients.http.authentication.client import get_authentication_client, AuthenticationClient


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()
