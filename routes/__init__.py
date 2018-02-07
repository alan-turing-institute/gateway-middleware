"""
Routes module
"""

from .routes import CasesApi, CaseApi, JobsApi, JobApi


def setup_routes(api):
    """
    Set up the routes for these api end points
    """
    api.add_resource(CasesApi, '/case')
    api.add_resource(CaseApi, '/case/<int:case_id>')
    api.add_resource(JobsApi, '/job')
    api.add_resource(JobApi, '/job/<int:job_id>')
