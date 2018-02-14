"""
Tests for the job api
"""
# flake8: noqa
# pylint: disable=W0613

from pytest import raises

from connection.api_schemas import JobPatchArgs
from marshmallow import ValidationError

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
    with raises(ValidationError):
        read = JobPatchArgs().load(input)

def test_invalid_args_fail(app):
    """
    Test that going of the end of pages still works
    """
    input = '{ "dog": "hound" }'
    with raises(ValidationError):
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
    with raises(ValidationError):
        read = JobPatchArgs().load(input)

@request_context("/case?fish=3")
def test_incorrect_pagination_args(app):
    result = app.dispatch_request()
    assert(result.status_code != 200)

@request_context("/job/2", method="PATCH",
                 content_type='application/json',
                 data='{"dog": "Awesome Job"}')
def test_rename_job_2(app):
    """
    Test that you can rename a job
    """
    result = JobApi().dispatch_request(2)
    print(result)
    assert(result['status'] != 'success')
    assert(len(result['changed']) == 0)
    assert(len(result['errors']) == 0)