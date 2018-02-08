"""
Tests for the job api
"""
# flake8: noqa
# pylint: disable=W0613

from pytest import raises
from werkzeug.exceptions import HTTPException

from routes import JobsApi, JobApi

from .decorators import request_context
from .fixtures import demo_app as app


@request_context("/job",
                 data='{"name": "bob", "case_id": "1", "author": "bob"}',
                 content_type='application/json', method="POST")
def test_create_job(app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert(result['job_id'] > 0)
