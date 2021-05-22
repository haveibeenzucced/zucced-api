"""Endpoints starting with /compromised_accounts/ are defined here.

This module contains all API endpoints which path contains '/compromised_accounts/'.
Not that no "business-logic" is defined in here, we simply pass in onto
the compromised_account service from the `service_factory`, by doing it this way
the controller only knows which methods it can call in compromised_account Service
but nothing about the database.
"""

import fastapi

from zucced_api.core import service_factory
from zucced_api.domain.compromised_accounts import compromised_account_schemas

router = fastapi.APIRouter()


ACCOUNT_SERVICE = fastapi.Depends(service_factory.get_compromised_account_services)


@router.get("/", response_model=compromised_account_schemas.Response)
async def get_compromised_accounts(
    facebook_id: str,
    service=ACCOUNT_SERVICE,
):
    return await service.get_by_id(account_id=facebook_id)
