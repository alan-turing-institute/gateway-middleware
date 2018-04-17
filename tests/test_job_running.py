"""
Tests for the job starting api
"""

# pylint: disable=I0011, W0611, W0621, W0613

from requests_mock import Mocker

from connection.constants import JOB_MANAGER_URL, JobStatus, RequestStatus
from connection.models import Job
from routes import JobApi, JobsApi, StatusApi
from .decorators import request_context
from .fixtures import demo_app as app


@request_context('/job',
                 data='{"name": "bob", "case_id": "1", "author": "bob"}',
                 content_type='application/json', method='POST')
def test_create_job(app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result['job_id'] == 2


@request_context('/job/2', method='POST')
def test_start_job_without_values(app):
    """
    Test that you can't start a job with unset values
    """
    with Mocker() as m:
        m.post(JOB_MANAGER_URL + '/2/start', json='data')
        result = JobApi().dispatch_request(2)
    assert len(result['errors']) > 0
    assert result['status'] == RequestStatus.FAILED.value
    assert Job.query.get(2).status == JobStatus.NOT_STARTED.value


@request_context('/job/1', method='POST')
def test_start_job(app):
    """
    Test that you can start a job
    """
    with Mocker() as m:
        m.post(JOB_MANAGER_URL + '/1/start', json='data')
        result = JobApi().dispatch_request(1)
    assert result['status'] == RequestStatus.SUCCESS.value
    assert Job.query.get(1).status == JobStatus.QUEUED.value


@request_context('/job/1/status', method='PUT',
                 data='{"status": "failed"}',
                 content_type='application/json')
def test_put_status(app):
    """
    Test that you can change the status of the queued job
    """
    result = StatusApi().dispatch_request(1)
    assert result['status'] == RequestStatus.SUCCESS.value
    assert Job.query.get(1).status == JobStatus.FAILED.value


@request_context('/job/2/status', method='PUT',
                 data='{"status": "failed"}',
                 content_type='application/json')
def test_fail_not_started(app):
    """
    Test that you can't fail a non started job
    """
    result = StatusApi().dispatch_request(2)
    assert result['status'] == RequestStatus.FAILED.value
    assert len(result['errors']) > 0
    assert Job.query.get(2).status == JobStatus.NOT_STARTED.value
