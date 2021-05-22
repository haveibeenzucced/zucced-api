"""This module is for all compromised_account related queries."""
from zucced_api.domain.compromised_accounts import compromised_account_model

Model = compromised_account_model.Model


class Queries(object):
    """Queries for compromised accounts."""

    async def get_by_id(self, account_id: str) -> Model:
        return await Model.get(account_id)
