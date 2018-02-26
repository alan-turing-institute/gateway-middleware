"""
Tests for the job api
"""
# flake8: noqa
# pylint: disable=W0613

from pytest import raises, mark

from connection.api_schemas import JobPatchArgs
from werkzeug.exceptions import HTTPException, BadRequestKeyError

from routes import JobApi

from .fixtures import demo_app as app
from .decorators import request_context


def test_extra_args_fail(app):
    """
    Test that going of the end of pages still works
    """
    input = {
        'name': 'fish',
        'dog': 'hound'
    }
    with raises(BadRequestKeyError):
        read = JobPatchArgs().load(input)

def test_invalid_args_fail(app):
    """
    Test that going of the end of pages still works
    """
    input = '{ "dog": "hound" }'
    with raises(BadRequestKeyError):
        read = JobPatchArgs().load(input)

def test_lists_check(app):
    """
    Test that extra args are rejected for lists
    """
    input = {
        "values": [
            {
                'name': "cat",
                'value': "siamese"
            }, {
                'name': "dog",
                'value': "bassett",
                'car': "Toyota"
            }
        ]
    }
    with raises(BadRequestKeyError):
        read = JobPatchArgs().load(input)

@request_context("/case?fish=3")
@mark.skip('Waiting on webargs bug')
def test_incorrect_pagination_args(app):
    with raises(HTTPException):
        result = app.dispatch_request()

@request_context("/job/2", method="PATCH",
                 content_type='application/json',
                 data='{"dog": "Awesome Job"}')
@mark.skip('Waiting on webargs bug')
def test_rename_job_2(app):
    """
    Test that you can't submit random arguments to 
    patch
    """
    with raises(HTTPException):
        result = JobApi().dispatch_request(2)
