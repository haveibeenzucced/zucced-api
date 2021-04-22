"""This module concerns itself with app creation."""

from fastapi import FastAPI
from fastapi.middleware import cors
import sentry_sdk
from sentry_sdk.integrations import sqlalchemy

from zucced_api.core import config_loader
from zucced_api.core.db import DB
from zucced_api.core import version
from zucced_api.routers import compromised_accounts_route


def create_app() -> FastAPI:
    """Create the app.

    Returns:
        FastAPI: Our instance of the FastAPI app.
    """
    app: FastAPI = FastAPI(title=config_loader.APP_NAME, version=version.__version__)
    _initalize_extensions(app=app)
    _add_middleware(app=app)
    return _register_routes(app=app)


def _add_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        middleware_class=cors.CORSMiddleware,
        allow_origins=config_loader.ALLOW_ORIGINS,
        allow_credentials=config_loader.ALLOW_CREDENTIALS,
        allow_methods=config_loader.ALLOW_METHODS,
        allow_headers=config_loader.ALLOW_HEADERS,
    )
    return app


def _register_routes(app: FastAPI) -> FastAPI:
    """Register routers.

    A router contains one or more routes.

    Args:
        app (FastAPI): app

    Returns:
        FastAPI: The app with registered routers.
    """
    app.include_router(
        router=compromised_accounts_route.router,
        tags=["Compromised Accounts"],
        prefix="/compromised_accounts",
    )
    return app


def _initalize_extensions(app: FastAPI):
    """_initalize_extensions.

    Args:
        app (FastAPI): app
    """
    DB.init_app(app=app)
    sentry_sdk.init(integrations=[sqlalchemy.SqlalchemyIntegration()])
