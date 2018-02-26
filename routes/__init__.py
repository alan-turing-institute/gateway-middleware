"""
Routes module
"""

from .case_routes import CasesApi, CaseApi
from .job_routes import JobsApi, JobApi
from .fake_routes import TestData


def setup_routes(api):
    """
    Set up the routes for these api end points
    """
    api.add_resource(CasesApi, '/case')
    api.add_resource(CaseApi, '/case/<int:case_id>')
    api.add_resource(JobsApi, '/job')
    api.add_resource(JobApi, '/job/<int:job_id>')

    # Only while in development
    api.add_resource(TestData, '/test')
