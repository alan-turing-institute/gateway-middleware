"""
Tests for the job starting api
"""
# flake8: noqa
# pylint: disable=W0613

from pytest import raises
from werkzeug.exceptions import HTTPException

from routes import JobApi

from .decorators import request_context
from .fixtures import demo_app as app
from connection.constants import RequestStatus


@request_context("/job/1", method="POST")
def test_start_job_without_values(app):
    """
    Test that you can't start a job with unset values
    """
    result = JobApi().dispatch_request(1)
    print(result)
    assert(len(result['errors']) > 0)
    assert(result['status'] == RequestStatus.FAILED.value)
