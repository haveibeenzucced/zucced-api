"""Module for configuring tests."""
import pathlib
import subprocess  # noqa: S404 used for specific command, should be fine.

import pytest
from starlette import testclient

from zucced_api import app as zucced_api_app


@pytest.fixture
def app():
    """Yield the app.

    Returns:
        app
    """
    return zucced_api_app.create_app()


@pytest.fixture
def client(app):  # noqa: WPS442
    """Get test client.

    Args:
        app: The zucced_api app.

    Yields:
        app: Yields an instance of the app after running migrations
    """
    cwd = pathlib.Path(__file__).parent.parent
    command = ["alembic", "upgrade", "head"]
    subprocess.check_call(command, cwd=cwd)  # noqa: S603, S607
    with testclient.TestClient(app) as test_client:
        yield test_client
