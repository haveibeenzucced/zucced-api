"""This module is for loading configuration into our internal representation."""

import uuid

from sqlalchemy.engine.url import URL
from starlette import config as starlette_config
from starlette import datastructures

config: starlette_config.Config = starlette_config.Config(".env")

DB_HOST: str = config("POSTGRES_HOST", default=None)
DB_PORT: int = config("POSTGRES_PORT", cast=int, default=None)
DB_USER: str = config("POSTGRES_USER", default=None)
DB_PASSWORD: datastructures.Secret = config(
    "POSTGRES_PASSWORD",
    cast=datastructures.Secret,
    default=None,
)
DB_DATABASE: str = config("POSTGRES_DB", default=None)
DB_DSN: URL = URL(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)

DEFAULT_DB_POOL_MIN_SIZE: int = 1
DB_POOL_MIN_SIZE: int = config(
    key="DB_POOL_MIN_SIZE",
    cast=int,
    default=DEFAULT_DB_POOL_MIN_SIZE,
)

DEFAULT_DB_POOL_MAX_SIZE: int = 16
DB_POOL_MAX_SIZE: int = config(
    key="DB_POOL_MAX_SIZE",
    cast=int,
    default=DEFAULT_DB_POOL_MAX_SIZE,
)

DB_ECHO: bool = config(key="DB_ECHO", cast=bool, default=False)
DB_SSL = config(key="DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST: bool = config(
    key="DB_USE_CONNECTION_FOR_REQUEST",
    cast=bool,
    default=True,
)

DEFAULT_RETRY_LIMIT: int = 32
DB_RETRY_LIMIT: int = config(
    key="DB_RETRY_LIMIT",
    cast=int,
    default=DEFAULT_RETRY_LIMIT,
)

DEFAULT_RETRY_INTERVAL: int = 1
DB_RETRY_INTERVAL: int = config(
    key="DB_RETRY_INTERVAL",
    cast=int,
    default=DEFAULT_RETRY_LIMIT,
)

SECRET_KEY: str = config(key="SECRET_KEY", default=str(uuid.uuid4()))
ALLOW_ORIGINS: datastructures.CommaSeparatedStrings = config(
    key="ALLOW_ORIGINS",
    default=["*"],
    cast=datastructures.CommaSeparatedStrings,
)
ALLOW_CREDENTIALS: bool = config(key="ALLOW_CREDENTIALS", cast=bool, default=True)
ALLOW_METHODS: datastructures.CommaSeparatedStrings = config(
    key="ALLOW_METHODS",
    default=["*"],
    cast=datastructures.CommaSeparatedStrings,
)
ALLOW_HEADERS: datastructures.CommaSeparatedStrings = config(
    key="ALLOW_HEADERS",
    default=["*"],
    cast=datastructures.CommaSeparatedStrings,
)

APP_NAME: str = config(key="APP_NAME", cast=str, default="Zucced API")
