import logging
from logging.config import fileConfig
import pathlib
import sys
import time

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Make the project importable noqa: isort skip
PROJECT_ROOT_DIR = str(pathlib.Path(__file__).parents[1])  # noqa: isort skip
sys.path.append(PROJECT_ROOT_DIR)  # noqa: isort skip

from zucced_api import app
from zucced_api.core.config_loader import DB_DSN
from zucced_api.core.config_loader import DB_RETRY_INTERVAL
from zucced_api.core.config_loader import DB_RETRY_LIMIT
from zucced_api.core.db import DB

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

zucced_app = app.create_app()
target_metadata = DB

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", str(DB_DSN))


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    print(DB_DSN)
    retries = 0
    while True:
        try:
            retries += 1
            connection = connectable.connect()
        except Exception:
            if retries < DB_RETRY_LIMIT:
                logging.info("Waiting for the database to start...")
                time.sleep(DB_RETRY_INTERVAL)
            else:
                logging.error("Max retries reached.")
                raise
        else:
            break

    with connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
