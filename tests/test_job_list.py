"""
Tests for the job api
"""

# pylint: disable=I0011, W0611, W0621, W0613

from pytest import raises
from werkzeug.exceptions import HTTPException

from connection.constants import JobStatus
from routes import JobApi, JobsApi
from .decorators import request_context, request_context_from_args
from .fixtures import demo_app, test_job_id


@request_context_from_args("/job/")
def test_get_job_routing(demo_app, test_job_id):
    """
    Test that a basic query of gets the specific job
    """
    result = demo_app.dispatch_request()
    assert result.status_code == 200
    # Data here is the JSON string
    assert result.data is not None
    assert len(result.data) > 0


@request_context("/job/5")
def test_get_no_such_job(demo_app):
    """
    Test that it fails to get a job that doesn't exist
    """
    with raises(HTTPException):
        demo_app.dispatch_request()


@request_context("/job?per_page=1", method="GET")
def test_1_per_page(demo_app):
    """
    Make sure that asking for one thing only gives you the first
    """
    result = JobsApi().dispatch_request()
    assert len(result.data) == 1
    assert result.data[0]["id"] is not None
    assert result.data[0]["status"] == JobStatus.NOT_STARTED.value
    assert result.data[0].get("values") is None


@request_context("/job?per_page=dog")
def test_per_page_string(demo_app):
    """
    Test that giving a string to per page fails
    """
    with raises(HTTPException):
        JobsApi().dispatch_request()


@request_context("/job?page=5")
def test_per_page_end(demo_app):
    """
    Test that going of the end of pages still works
    """
    result = JobsApi().dispatch_request()
    assert len(result.data) == 0


@request_context("/job", method="GET")
def test_per_page(demo_app):
    """
    Make sure you get multiple jobs if you ask without limiting
    """
    result = JobsApi().dispatch_request()
    assert len(result.data) == 2


@request_context(
    "/job",
    data='{"name": "bob", "case_id": "1", "author": "bob"}',
    content_type="application/json",
    method="POST",
)
def test_create_job(demo_app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result["job_id"] is not None
