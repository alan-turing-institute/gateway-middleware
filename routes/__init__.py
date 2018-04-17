"""
Routes module
"""

from connection.constants import StatusConverter
from .case_routes import CaseApi, CasesApi
from .fake_routes import TestData
from .job_routes import JobApi, JobsApi, StatusApi


def setup_routes(app, api):
    """
    Set up the routes for these api end points
    """
    app.url_map.converters['stat'] = StatusConverter

    api.add_resource(CasesApi, '/case')
    api.add_resource(CaseApi, '/case/<int:case_id>')
    api.add_resource(JobsApi, '/job')
    api.add_resource(JobApi, '/job/<int:job_id>')
    api.add_resource(StatusApi, '/job/<int:job_id>/status')

    # Only while in development
    api.add_resource(TestData, '/test')
