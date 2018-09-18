"""
Helper functions for the routes
"""


from connection.constants import RequestStatus


def make_response(response=RequestStatus.SUCCESS, messages=[], errors=[], data=None):
    """
    Make a response dictionary to return to the user
    """
    template = {"status": response.value, "messages": messages, "errors": errors}
    if data:
        template["data"] = data
    return template
