"""Helper methods for users."""
import time

from faker import Faker
from faker.providers import person

FAKE = Faker()
FAKE.add_provider(person)


def random_user() -> dict:
    """Get a random user dict.

    Returns:
        dict: User as a dictionary
    """
    name = FAKE.first_name()
    email = "{name}.{rand_int}@siemens.com".format(name=name, rand_int=int(time.time()))
    return {"name": name, "email": email, "password": "OkMakker1@"}


def authenticate(client, email: str, password: str, token: str):
    """Call the authenticate endpoint.

    Args:
        client: Test client.
        email: str
        password: str
        token: str

    Returns:
        Response: the request response.
    """
    return client.post(
        "/users/token",
        json={"email": email, "password": password, "token": token},
    )


def register(client, user_model=None):
    """Call the register endpoint.

    Args:
        client: Test client.
        user_model: Optional user_model, if None provided it will use random_user().

    Returns:
        Response: the request response.
    """
    if user_model is None:
        user_model = random_user()
    return client.post("/users/register", json=user_model)


def verify(client, token: str):
    """Call the register endpoint.

    Args:
        client: Test client.
        token: The token to verify.

    Returns:
        Response: the request response.
    """
    return client.get("/users/verify", params={"token": token})
