"""
Tests for the job starting api
"""

# pylint: disable=W0613

from routes import JobApi, JobsApi

from .decorators import request_context
from .fixtures import demo_app as app  # flake8: noqa
from connection.constants import RequestStatus, JOB_MANAGER_URL

from requests_mock import Mocker

@request_context("/job",
                 data='{"name": "bob", "case_id": "1", "author": "bob"}',
                 content_type='application/json', method="POST")
def test_create_job(app):
    """
    Test that a job is created
    """
    result = JobsApi().dispatch_request()
    assert(result['job_id'] == 2)

@request_context('/job/2', method='POST')
def test_start_job_without_values(app):
    """
    Test that you can't start a job with unset values
    """
    with Mocker() as m:
        m.post(JOB_MANAGER_URL + '/2/start', json='data')
        result = JobApi().dispatch_request(2)
    assert(len(result['errors']) > 0)
    assert(result['status'] == RequestStatus.FAILED.value)

@request_context('/job/1', method='POST')
def test_start_job(app):
    """
    Test that you can start a job
    """
    with Mocker() as m:
        m.post(JOB_MANAGER_URL + '/1/start', json='data')
        result = JobApi().dispatch_request(1)
    print(result)
    assert(result['status'] == RequestStatus.SUCCESS.value)
