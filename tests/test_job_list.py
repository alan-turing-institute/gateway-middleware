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
from connection.constants import JobStatus


@request_context("/job/1")
def test_get_job_routing(app):
    """
    Test that a basic query of gets the specific job
    """
    result = app.dispatch_request()
    assert(result.status_code == 200)
    # Data here is the JSON string
    assert(result.data is not None)
    assert(len(result.data) > 0)


@request_context("/job/5")
def test_get_no_such_job(app):
    """
    Test that it fails to get a job that doesn't exist
    """
    with raises(HTTPException):
        result = app.dispatch_request()


@request_context("/job/dog")
def test_get_string_jobname(app):
    """
    Test that getting a job that isn't a number fails
    """
    with raises(HTTPException):
        result = app.dispatch_request()


@request_context("/")
def test_get_job_1(app):
    """
    Get get job 1 and make sure you get something
    sensible back
    """
    result = JobApi().dispatch_request(1)
    print(result.data)
    assert(len(result.data['values']) > 0)
    assert(result.data['id'] == 1)
    assert(result.data['status'] == JobStatus.NOT_STARTED.value)


@request_context("/job?per_page=1", method="GET")
def test_1_per_page(app):
    """"
    Make sure that asking for one thing only gives you the first
    """
    result = JobsApi().dispatch_request()
    assert(len(result.data) == 1)
    assert(result.data[0]['id'] == 1)
    assert(result.data[0]['status'] == JobStatus.NOT_STARTED.value)
    assert(result.data[0].get('values') is None)


@request_context("/job?per_page=dog")
def test_per_page_string(app):
    """
    Test that giving a string to per page fails
    """
    with raises(HTTPException):
        result = JobsApi().dispatch_request()


@request_context("/job?page=dog")
def test_per_page_string(app):
    """
    Test that giving a string to page fails
    """
    with raises(HTTPException):
        result = JobsApi().dispatch_request()

@request_context("/job?page=5")
def test_per_page_string(app):
    """
    Test that going of the end of pages still works
    """
    result = JobsApi().dispatch_request()
    assert(len(result.data) == 0)


@request_context("/job", method="GET")
def test_per_page(app):
    """
    Make sure you get multiple jobs if you ask without limiting
    """
    result = JobsApi().dispatch_request()
    assert(len(result.data) == 1)


@request_context("/job",
                 data='{"name": "bob", "case_id": "1", "author": "bob"}',
                 content_type='application/json', method="POST")
def test_create_job(app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert(result['job_id'] > 0)
