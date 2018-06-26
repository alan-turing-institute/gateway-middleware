"""
Routes module
"""

from connection.constants import StatusConverter
from .case_routes import CaseApi, CasesApi
from .fake_routes import TestData
from .job_routes import JobApi, JobsApi, OutputApi, StatusApi


def set_up_routes(app, api):
    """
    Set up the routes for these api end points
    """
    app.url_map.converters['stat'] = StatusConverter

    api.add_resource(CasesApi, '/case')
    api.add_resource(CaseApi, '/case/<int:case_id>')
    api.add_resource(JobsApi, '/job')
    api.add_resource(JobApi, '/job/<string:job_id>')
    api.add_resource(StatusApi, '/job/<string:job_id>/status')
    api.add_resource(OutputApi, '/job/<string:job_id>/output')

    # Only while in development
    api.add_resource(TestData, '/test')
