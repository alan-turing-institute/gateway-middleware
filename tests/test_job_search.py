"""
Tests for the job search api
"""

# pylint: disable=I0011, W0611, W0621, W0613

import pytest
from pytest import raises
from werkzeug.exceptions import HTTPException

from routes import JobsApi, JobsSearchApi
from .decorators import request_context, request_context_from_args
from .fixtures import demo_app, test_job_id


setup = ["test_create_job_alice", "test_create_job_bob"]


@request_context(
    "/job",
    data='{"name": "alice test", "case_id": "1", "author": "alice"}',
    content_type="application/json",
    method="POST",
)
def test_create_job_alice(demo_app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result["job_id"] is not None


@request_context(
    "/job",
    data='{"name": "bob test", "case_id": "1", "author": "bob"}',
    content_type="application/json",
    method="POST",
)
def test_create_job_bob(demo_app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result["job_id"] is not None


@pytest.mark.dependency(depends=setup)
@request_context("/job/search?name=alice+test&exact=true")
def test_search_exact(demo_app):
    """
    Exact search for a job with a given name.
    """
    result = JobsSearchApi().dispatch_request()

    # single job is returned
    assert len(result.data) == 1

    # job name corresponds to search name
    assert result.data[0]["name"] == "alice test"


@pytest.mark.dependency(depends=setup)
@request_context("/job/search?name=alice")
def test_search_partial(demo_app):
    """
    Partial search for a job with a given name fragment.
    """
    result = JobsSearchApi().dispatch_request()

    # single job is returned
    assert len(result.data) == 1

    # job name corresponds to search name
    assert result.data[0]["name"] == "alice test"
