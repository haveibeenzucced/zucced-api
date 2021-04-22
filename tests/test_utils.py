"""This module provides testing utility features."""
import datetime
import logging
import time
from typing import Any, Dict, Tuple

from starlette import status

LOGGER = logging.getLogger(__name__)
MAX_RESPONSE_TIME = 200


def raise_for_status(func):
    """Decorator that raises a status upon error.

    Args:
        func: The function to be wrapped in the decorator.

    Returns:
        The decorated function.
    """

    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        LOGGER.info(
            "Called wrapper with function: '{name}'.".format(name=func.__name__),
        )
        response = func(*args, **kwargs)
        LOGGER.info(
            "response saved, status code: {status_code}".format(
                status_code=response.status_code,
            ),
        )
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            LOGGER.info(response.json()["detail"])
        response.raise_for_status()
        return response.json(), response.status_code

    return wrapper


def time_it(func):
    """Decorator to time function calls.

    Args:
        func: The function that should be wrapped

    Returns:
        The decorated function.
    """

    def wrapper(*args, **kwargs):
        started = time.time()
        func_result = func(*args, **kwargs)
        elapsed_seconds = time.time() - started
        elapsed_ms = round(elapsed_seconds * 1000)
        LOGGER.info(
            "{func_name} took {elapsed_ms} ms to execute.".format(
                func_name=func.__name__,
                elapsed_ms=elapsed_ms,
            ),
        )
        assert elapsed_ms < MAX_RESPONSE_TIME
        return func_result

    return wrapper


def no_state_change(new_data: Dict[str, Any], old_data: Dict[str, Any]) -> None:
    """Check if two data models are relatively similiar.

    Args:
        new_data (Dict[str, Any]): bla bla
        old_data (Dict[str, Any]): bla bla
    """
    for key, item_value in old_data.items():  # noqa: WPS327
        # Timezones can be different, but could still be correct:
        try:  # noqa: WPS229
            model_dt = datetime.datetime.fromisoformat(item_value)
            data_dt = datetime.datetime.fromisoformat(new_data[key])
            assert model_dt == data_dt
        except TypeError:
            assert item_value == new_data[key]
        except ValueError:
            continue
