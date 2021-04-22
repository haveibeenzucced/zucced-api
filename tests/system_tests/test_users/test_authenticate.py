"""This module is for testing the `/users/token` endpoint."""
from typing import Optional

import pyotp
from starlette import status

from tests.system_tests.test_users import user_helper


def login_request(
    client,
    password: Optional[str] = None,
    email: Optional[str] = None,
    token: Optional[str] = None,
):
    """Fixture for login request.

    Args:
        password (Optional[str]): Overload password
        email (Optional[str]): Overload email
        token (Optional[str]): Overload token
        client: Test client

    Returns:
        Dict[email: str, password: str, token: str]
    """
    user_model = user_helper.random_user()
    response = user_helper.register(client=client, user_model=user_model)

    assert response.status_code == status.HTTP_201_CREATED
    return {
        "email": email or user_model["email"],
        "password": password or user_model["password"],
        "token": token or _get_token(response=response),
    }


def test_valid_login(client):  # noqa: WPS442
    """Test if we get 201 CREATED status code when creating a user.

    Args:
        client: Test client.

    Returns:
        dict: response body
    """
    user = login_request(client=client)
    auth_response = user_helper.authenticate(client=client, **user)

    assert auth_response.status_code == status.HTTP_200_OK
    return auth_response.json()


def test_wrong_password(client):  # noqa: WPS442
    """Test if get 401 UNAUTHORIZED when we provide a wrong password.

    Args:
        client: Test client.
    """
    user = login_request(  # noqa: S106 (test password, not critical)
        client=client,
        password="wronG123%!4",
    )
    auth_response = user_helper.authenticate(client=client, **user)

    assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_wrong_email(client):  # noqa: WPS442
    """Test if get 401 UNAUTHORIZED when we provide a wrong email.

    Args:
        client: Test client.
    """
    user = login_request(client=client, email="test@test.dk")
    auth_response = user_helper.authenticate(client=client, **user)

    assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_wrong_token(client):  # noqa: WPS442
    """Test if get 401 UNAUTHORIZED when we provide a wrong token.

    Args:
        client: Test client.
    """
    user = login_request(  # noqa: S106 (test token, not critical)
        client=client,
        token="123456",
    )
    auth_response = user_helper.authenticate(client=client, **user)

    assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED


def _get_token(response):
    totp_uri = response.json()["totp_uri"]
    totp = pyotp.parse_uri(totp_uri)
    return totp.now()
