"""
Helper functions for the routes
"""

from typing import List

from connection.constants import RequestStatus


def make_response(
    response: RequestStatus = RequestStatus.SUCCESS,
    messages: List[str] = [],
    errors: List[str] = [],
) -> dict:
    """
    Make a response dictionary to return to the user
    """
    return {"status": response.value, "data": messages, "errors": errors}
