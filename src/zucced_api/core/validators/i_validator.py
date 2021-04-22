"""This module is used for the interface validator."""
import abc
from typing import Any


class ValidatorInterface(object, metaclass=abc.ABCMeta):
    """Interface for our custom validators."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Checks if classes that inherit this have implemented it properly.

        Args:
            subclass: The hooked sub class.

        Returns:
            bool: True if implemented, raises error if not.
        """
        return (
            hasattr(subclass, "validate")  # noqa: WPS421
            and callable(
                subclass.validate,
            )
        ) or NotImplemented

    @abc.abstractmethod
    def validate(self, to_be_validated: Any):
        """Implement business logic here.

        Args:
            to_be_validated (Any): The object to be validated by the validator.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError
