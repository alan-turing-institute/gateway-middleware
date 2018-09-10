"""
Tests for the job api
"""
# pylint: disable=I0011, W0611, W0621, W0613

from pytest import mark, raises
from werkzeug.exceptions import BadRequestKeyError, HTTPException

from connection.api_schemas import JobPatchArgs
from routes import JobApi
from .decorators import request_context
from .fixtures import demo_app as app


def test_extra_args_fail(app):
    """
    Test that going of the end of pages still works
    """
    test_input = {"name": "fish", "dog": "hound"}
    with raises(BadRequestKeyError):
        JobPatchArgs().load(test_input)


def test_invalid_args_fail(app):
    """
    Test that going of the end of pages still works
    """
    test_input = '{ "dog": "hound" }'
    with raises(BadRequestKeyError):
        JobPatchArgs().load(test_input)


def test_lists_check(app):
    """
    Test that extra args are rejected for lists
    """
    test_input = {
        "values": [
            {"name": "cat", "value": "siamese"},
            {"name": "dog", "value": "bassett", "car": "Toyota"},
        ]
    }
    with raises(BadRequestKeyError):
        JobPatchArgs().load(test_input)


@request_context("/case?fish=3")
@mark.skip("Waiting on webargs bug")
def test_incorrect_pagination_args(app):
    """
    Throw an exception if unused arguments are provided
    in a request.
    """
    with raises(HTTPException):
        app.dispatch_request()


@request_context(
    "/job/2",
    method="PATCH",
    content_type="application/json",
    data='{"dog": "Awesome Job"}',
)
@mark.skip("Waiting on webargs bug")
def test_rename_job_2(app):
    """
    Test that you can't submit random arguments to
    patch
    """
    with raises(HTTPException):
        JobApi().dispatch_request(2)
