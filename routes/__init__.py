"""
Routes module
"""

from .case_routes import CasesApi, CaseApi
from .job_routes import JobsApi, JobApi, StatusApi
from .fake_routes import TestData
from connection.constants import StatusConverter


def setup_routes(app, api):
    """
    Set up the routes for these api end points
    """

    app.url_map.converters['stat'] = StatusConverter

    api.add_resource(CasesApi, '/case')
    api.add_resource(CaseApi, '/case/<int:case_id>')
    api.add_resource(JobsApi, '/job')
    api.add_resource(JobApi, '/job/<int:job_id>')
    api.add_resource(StatusApi, '/job/<int:job_id>/<stat:status>')

    # Only while in development
    api.add_resource(TestData, '/test')
