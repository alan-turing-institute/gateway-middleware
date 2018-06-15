"""
Tests for the job starting api
"""

# pylint: disable=I0011, W0611, W0621, W0613

from requests_mock import Mocker

from connection.constants import JobStatus, RequestStatus
from connection.models import Job
from routes import JobApi, JobsApi, StatusApi
from .decorators import request_context
from .fixtures import demo_app, test_job_id, test_job_id_no_values


@request_context('/job',
                 data='{"name": "bob", "case_id": "1", "author": "bob"}',
                 content_type='application/json', method='POST')
def test_create_job(demo_app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert result['job_id'] is not None


@request_context('/job/2', method='POST')
def test_start_job_without_values(demo_app, test_job_id_no_values):
    """
    Test that you can't start a job with unset values
    """
    with Mocker() as m:
        start_url = '{}/{}/start'.format(
            demo_app.config['JOB_MANAGER_URL'],
            test_job_id_no_values)
        m.post(start_url, json='data')
        result = JobApi().dispatch_request(test_job_id_no_values)
    assert len(result['errors']) > 0
    assert result['status'] == RequestStatus.FAILED.value
    assert Job.query.get(test_job_id_no_values).status == \
        JobStatus.NOT_STARTED.value


@request_context('/job/1', method='POST')
def test_start_job(demo_app, test_job_id):
    """
    Test that you can start a job
    """
    with Mocker() as m:
        start_url = '{}/{}/start'.format(
            demo_app.config['JOB_MANAGER_URL'], test_job_id)
        m.post(start_url, json='data')
        result = JobApi().dispatch_request(test_job_id)
    assert result['status'] == RequestStatus.SUCCESS.value
    assert Job.query.get(test_job_id).status == JobStatus.QUEUED.value


@request_context('/job/1/status', method='PUT',
                 data='{"status": "failed"}',
                 content_type='application/json')
def test_put_status(demo_app, test_job_id):
    """
    Test that you can change the status of the queued job
    """
    result = StatusApi().dispatch_request(test_job_id)
    assert result['status'] == RequestStatus.SUCCESS.value
    assert Job.query.get(test_job_id).status == JobStatus.FAILED.value


@request_context('/job/2/status', method='PUT',
                 data='{"status": "failed"}',
                 content_type='application/json')
def test_fail_not_started(demo_app, test_job_id_no_values):
    """
    Test that you can't fail a non started job
    """
    result = StatusApi().dispatch_request(test_job_id_no_values)
    assert result['status'] == RequestStatus.FAILED.value
    assert len(result['errors']) > 0
    assert Job.query.get(test_job_id_no_values).status == \
        JobStatus.NOT_STARTED.value
