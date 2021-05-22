"""This module is for schemas related to compromised_accounts."""
import pydantic


class Response(pydantic.BaseModel):
    """Response schema that indicates if the user has been compromised."""

    compromised: bool
