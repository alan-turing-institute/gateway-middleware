"""
Tests for the job api

This file requires that the tests
are run in the order they are written.
"""

# pylint: disable=I0011, W0611, W0621, W0613
from uuid import uuid4

import unittest

from werkzeug.exceptions import HTTPException

from connection import init_database
from connection.constants import JobStatus, RequestStatus
from connection.models import Job, db
from routes import JobApi, JobsApi
from .decorators import request_context, request_context_from_args
from .fixtures import demo_app
from .fixtures import test_job_id


@request_context('/job',
                 data='{"name": "bobby", "case_id": "1", "author": "bobo"}',
                 content_type='application/json', method='POST')
def test_create_job(demo_app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result['job_id'] is not None



@request_context('/job/2')
def test_has_new_job(demo_app, test_job_id):
    """
    Test that the new job is there
    """
    result = JobApi().dispatch_request(test_job_id)
    assert result.data['id'] == test_job_id
    assert result.data['name'] == 'bob'


@request_context('/job/2', method='PATCH',
                 content_type='application/json',
                 data='{"name": "Awesome Job"}')
def test_rename_job_2(demo_app,test_job_id):
    """
    Test that you can rename a job
    """
    result = JobApi().dispatch_request(test_job_id)
    assert result['status'] == 'success'
    assert result['changed'][0] == 'name'
    assert len(result['changed']) == 1
    assert len(result['errors']) == 0


@request_context('/job/2')
def test_job_renamed(demo_app, test_job_id):
    """
    Test that the job name has actually changed
    """
    result = JobApi().dispatch_request(test_job_id)
    assert result.data['id'] == test_job_id
    assert result.data['name'] == 'Awesome Job'


@request_context('/job/2', method='PATCH',
                 content_type='application/json',
                 data='{"values": [ { "name": "length", "value": "100" }]}')
def test_revalues_job_2(demo_app, test_job_id):
    """
    Test that you can't set an invalid number
    """
    result = JobApi().dispatch_request(test_job_id)
    print(result)
    assert result['changed'] == []
    assert result['status'] == 'failed'
    assert len(result['errors']) > 0


@request_context('/job/2', method='PATCH',
                 content_type='application/json',
                 data='{"values": [ { "name": "length", "value": "10" }]}')
def test_good_revalues_job_2(demo_app, test_job_id):
    """
    Test that you can't set an invalid number
    """
    result = JobApi().dispatch_request(test_job_id)
    print(result)
    assert result['changed'] == ['values']
    assert result['status'] == 'success'
    assert len(result['errors']) == 0


@request_context_from_args('/job/')
def test_get_job_1(demo_app,test_job_id):
    """
    Get get job 1 and make sure you get something sensible back
    """
    result = JobApi().dispatch_request(test_job_id)
    print(result)
    assert len(result.data['values']) > 0
    assert result.data['id'] == test_job_id
    assert result.data['status'] == JobStatus.NOT_STARTED.value


@request_context('/job/2', method='PATCH',
                 content_type='application/json',
                 data='{"description": "test description"}')
def test_redescribe_job_2(demo_app, test_job_id):
    """
    Test that you can change description of job
    """
    result = JobApi().dispatch_request(test_job_id)
    print(result)
    assert result['status'] == RequestStatus.SUCCESS.value
    assert result['changed'] == ['description']
    assert len(result['errors']) == 0
    assert Job.query.get(test_job_id).description == 'test description'


@request_context('/job/2', method='PATCH',
                 content_type='application/json',
                 data='{"description": "    "}')
def test_undescribe_job_2(demo_app, test_job_id):
    """
    Test that you cannot put empty values into description
    """
    result = JobApi().dispatch_request(test_job_id)
    print(result)
    assert result['status'] == RequestStatus.FAILED.value
    assert result['changed'] == []
    assert len(result['errors']) > 0
    assert Job.query.get(test_job_id).description == 'test description'
