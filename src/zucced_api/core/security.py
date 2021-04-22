"""This module is for security and cryptographic related stuff."""
import datetime
from typing import Optional

from jose import jwt
from passlib import context

from zucced_api.core import config_loader
from zucced_api.core.exceptions import token_exceptions


class SecurePassword(object):
    """Adds hashing (with salting) and verification capabilities to a clear text password."""

    _password_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_and_salt_password(self, password: str) -> str:
        """Hash and salt a clear text password using bcrypt.

        Args:
            password (str): Plain text password

        Returns:
            str: Password hash
        """

        return self._password_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password.

        Args:
            password (str): Clear text password.
            password_hash (str): Salted and hashed password.

        Returns:
            bool: True if the plain text password is correct.
        """

        return self._password_context.verify(secret=password, hash=password_hash)


class Token(object):
    """Adds the option to create and verify tokens."""

    _algorithm = "HS256"

    def create(self, email: str, expires_delta: Optional[datetime.timedelta] = None) -> str:
        """Creates an access token that is valid for 15 minutes.

        Args:
            email (str): email to encode into the token.
            expires_delta (Optional[datetime.timedelta]): Time before token expires.

        Returns:
            str: encoded JWT token.
        """

        expiration_time = self._get_expiration_time(expires_delta=expires_delta)
        to_encode = {"sub": email, "exp": expiration_time}
        return jwt.encode(to_encode, config_loader.SECRET_KEY, algorithm=self._algorithm)

    def verify(self, token: str) -> str:
        """Verifies an access token by decoding it.

        Args:
            token (str): the token to be validated.

        Raises:
            InvalidToken: Is raised if we cannot decrypt it.

        Returns:
            str: encoded JWT token.
        """
        try:
            return self._decode(token=token)
        except (jwt.JWTError, jwt.JWSError):
            raise token_exceptions.InvalidToken()

    def _get_expiration_time(self, expires_delta: Optional[datetime.timedelta] = None) -> datetime.datetime:
        if expires_delta:
            return datetime.datetime.utcnow() + expires_delta

        timedelta = datetime.timedelta(minutes=config_loader.TOKEN_VALID_MINUTES)

        return datetime.datetime.utcnow() + timedelta

    def _decode(self, token: str):
        payload = jwt.decode(token, config_loader.SECRET_KEY, algorithms=[self._algorithm])
        return payload["sub"]
