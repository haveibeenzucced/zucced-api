"""This module is for custom password exceptions.

To make the exceptions layer as independant as possible on the chosen framework we inherit the exceptions
we would normally raise from the relevant current framework and then raise the inherited class instead.
By doing it this way we make it easier to swap to another framework in the future, since we only have
to change all the exceptions one place.
"""
