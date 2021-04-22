"""This module is for implementing compromised_account services.

The Service class' job is to interface with the compromised_account queries, and
transform the result provided by the Quries class into Schemas. When
creating an instance of Service() you shouldn't call
`service._queries()` directly, hence why it's declared as private (_).
"""
from zucced_api.domain.compromised_accounts import compromised_account_queries, compromised_account_schemas
from zucced_api.core.exceptions import http_exceptions


class Service:
    """Service."""

    def __init__(self, queries: compromised_account_queries.Queries):
        """__init__.

        Args:
            queries (compromised_account_queries.Queries): queries
        """
        self._queries = queries

    async def get_by_id(
            self, account_id: str) -> compromised_account_schemas.Response:
        """Gets the compromised_account that matches the provided account_id.

        Args:
            account_id (str): account_id
        Returns:
            compromised_account_schemas.Response: If the compromised_account is found, otherwise 404.
        """
        compromised_account = await self._queries.get_by_id(account_id=account_id)
        if compromised_account is None:
            raise http_exceptions.NotFound()
        return compromised_account_schemas.Response.from_orm(compromised_account)
