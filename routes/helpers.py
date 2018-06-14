"""
Helper functions for the routes
"""

from typing import List
from functools import wraps

from flask import request, Response, current_app
import requests
from connection.constants import RequestStatus


def make_response(response: RequestStatus=RequestStatus.SUCCESS,
                  messages: List[str]=[], errors: List[str]=[]) -> dict:
    """
    Make a response dictionary to return to the user
    """
    return {
        'status': response.value,
        'data': messages,
        'errors': errors
    }


def token_required(f):
    """Checks whether token is valid or raises error 401."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_string = request.headers.get('Authorization')

        auth_url = current_app.config['AUTHENTICATION_URL']
        r = requests.get(auth_url, headers={'Authorization': token_string})

        if r.status_code == 200:
            return f(*args, **kwargs)
        else:
            return Response(
                'User not authenticated',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated
