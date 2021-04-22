"""This module is for testing the `/users/token` endpoint."""
from starlette import status

from tests.system_tests.test_users import test_authenticate
from tests.system_tests.test_users import user_helper


def test_correct_token(client):  # noqa: WPS442
    """Test if get 200 OK when verifying a valid token.

    Args:
        client: Test client.
    """
    token = test_authenticate.test_valid_login(client=client)["access_token"]
    auth_response = user_helper.verify(client=client, token=token)

    assert auth_response.status_code == status.HTTP_200_OK


def test_invalid_token(client):  # noqa: WPS442
    """Test if we get 401 UNAUTHORIZED status code when trying to verify an invalid token.

    Args:
        client: Test client.
    """
    auth_response = user_helper.verify(  # noqa: S106 (invalid hardcoded token)
        client=client,
        token="123jklasdkl123",
    )
    assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED
