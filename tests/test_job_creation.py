"""
Tests for the job api

This files requires that the tests
are run in the order they are written.
"""
# flake8: noqa
# pylint: disable=W0613

from pytest import raises
from werkzeug.exceptions import HTTPException

from routes import JobsApi, JobApi

from connection.models import Job

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
    assert(result['job_id'] == 2)


@request_context("/job/2")
def test_has_new_job(app):
    """
    Test that the new job is there
    """
    result = JobApi().dispatch_request(2)
    assert(result.data['id'] == 2)
    assert(result.data['name'] == 'bob')


@request_context("/job/2", method="PATCH",
                 content_type='application/json',
                 data='{"name": "Awesome Job"}')
def test_rename_job_2(app):
    """
    Test that you can rename a job
    """
    result = JobApi().dispatch_request(2)
    assert(result['status'] == 'success')
    assert(result['changed'][0] == 'name')
    assert(len(result['changed']) == 1)
    assert(len(result['errors']) == 0)


@request_context("/job/2")
def test_job_renamed(app):
    """
    Test that the job name has actually changed
    """
    result = JobApi().dispatch_request(2)
    assert(result.data['id'] == 2)
    assert(result.data['name'] == "Awesome Job")


@request_context("/job/2", method="PATCH",
                 content_type='application/json',
                 data='{"values": [ { "name": "length", "value": "100" }]}')
def test_revalues_job_2(app):
    """
    Test that you can't set an invalid number
    """
    result = JobApi().dispatch_request(2)
    print(result)
    assert(result['changed'] == [])
    assert(result['status'] == 'failed')
    assert(len(result['errors']) > 0)
