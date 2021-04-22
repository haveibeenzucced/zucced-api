"""This module is for testing the `/users/register` endpoint."""
from starlette import status

from tests.system_tests.test_users import user_helper


def test_valid_status_code(client):
    """Test if we get 201 CREATED status code when creating a user.

    Args:
        client: Test client.
    """
    response = user_helper.register(client)
    assert response.status_code == status.HTTP_201_CREATED


def test_conflict(client):
    """Test if by registering two identical users that we get a 409 CONFLICT status code.

    Args:
        client: Test client.
    """
    user_model = user_helper.random_user()
    user_helper.register(client=client, user_model=user_model)
    response = user_helper.register(client=client, user_model=user_model)
    assert response.status_code == status.HTTP_409_CONFLICT
