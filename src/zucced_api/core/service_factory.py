"""This module is for adding service factories for all services."""
from zucced_api.domain.compromised_accounts import compromised_account_queries
from zucced_api.domain.compromised_accounts import compromised_account_services


def get_compromised_account_services() -> compromised_account_services.Service:
    """Get an instance of compromised_account service.

    Returns:
        compromised_account_services.Service: The User service.

    """
    return compromised_account_services.Service(compromised_account_queries.Queries())
