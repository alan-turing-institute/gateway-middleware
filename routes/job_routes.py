"""
Defintions of routes for the app
"""

from flask_restful import abort, Resource
import requests
from sqlalchemy.exc import IntegrityError
from webargs import missing
from webargs.flaskparser import use_kwargs

from connection.api_schemas import (JobArgs, JobPatchArgs,
                                    PaginationArgs, StatusPatchSchema)
from connection.constants import JOB_MANAGER_URL, JobStatus, RequestStatus
from connection.models import db, Job
from connection.schemas import JobHeaderSchema, JobSchema
from .helpers import make_response

job_header_schema = JobHeaderSchema()
job_schema = JobSchema()


class JobsApi(Resource):
    """
    Endpoint for dealing with the list of jobs
    """

    @use_kwargs(JobArgs(), locations=('json',))
    def post(self, case_id, name, author):
        """
        Create a new job based on a case
        """
        try:
            new_job = Job(name=name,
                          user=author, case_id=case_id)
            db.session.add(new_job)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            abort(404,
                  message='Sorry, these parameters have already been used')
        return {'job_id': new_job.id}

    @use_kwargs(PaginationArgs())
    def get(self, page, per_page):
        """
        Get all the jobs that are in the requested range
        """
        return job_header_schema.dump(Job.query.paginate(page, per_page,
                                                         False).items,
                                      many=True)


class JobApi(Resource):
    """
    Endpoint for dealing with a specific job
    """

    def get(self, job_id):
        """
        Get the specified job
        """
        try:
            job_id = int(job_id)
        except ValueError as e:
            print(e)
            abort(404, message='Sorry no job id {}'. format(job_id))
        job = Job.query.get(job_id)
        if job is not None:
            return job_schema.dump(job)
        else:
            abort(404, message='Sorry, jobs {} not found'.format(job_id))
            return None

    @use_kwargs(JobPatchArgs())
    def patch(self, job_id, name, description, values):
        """
        Update the given details for this job
        """
        changed = []
        error_log = []
        status = RequestStatus.SUCCESS.value
        if name is missing and values is missing and description is missing:
            # You don't actually need to change anything
            return {
                'status': status,
                'changed': changed,
                'errors': error_log
            }
        job = Job.query.get(job_id)
        if job is None:
            abort(404, message='Sorry, job {} not found'.format(job_id))
        if name is not missing:
            if job.set_name(name, error_log):
                changed.append('name')
        if description is not missing:
            if job.set_description(description, error_log):
                changed.append('description')
        if values is not missing:
            if job.set_value_list(values, error_log):
                changed.append('values')
        try:
            if len(error_log) == 0:
                db.session.commit()
            else:
                db.session.rollback()
                changed = []
                status = RequestStatus.FAILED.value
        except IntegrityError as e:
            print(e)
            abort(404, message='Sorry. Failed to commit your request')
        return {
            'status': status,
            'changed': changed,
            'errors': error_log
        }

    def post(self, job_id):
        """
        Start the given job if it isn't started yet
        """
        job = Job.query.get(job_id)
        if job is None:
            abort(404, message='Sorry, job {} not found'.format(job_id))
        if job.status != JobStatus.NOT_STARTED.value:
            return make_response(RequestStatus.FAILED,
                                 errors=['Job already started'])
        if not job.fully_configured():
            return make_response(RequestStatus.FAILED,
                                 errors=['You must set all parameters '
                                         'before starting a job'])
        params = {
            'fields_to_patch': job.field_list(),
            'scripts': job.script_list(),
            'username': job.user
        }
        response = requests.post('{}/job/{}/start'.format(JOB_MANAGER_URL, job_id),
                                 json=params)
        if response.status_code != 200:
            return make_response(RequestStatus.FAILED,
                                 errors=['Job Manager returned HTTP {}'
                                         .format(response.status_code)])

        # TODO: do something with: result = response.json
        # TODO: Handle non http errors - but they haven't been implemented
        job.status = JobStatus.QUEUED.value
        db.session.commit()
        return make_response()


class StatusApi(Resource):
    """
    This class deals with status changes to jobs
    """

    @use_kwargs(StatusPatchSchema())
    def put(self, job_id: int, status: str):
        """
        Set the status for the given job
        """
        try:
            status = JobStatus[status.upper()]
        except KeyError:
            abort(400, message='Unknown status {}'.format(status))

        job = Job.query.get(job_id)
        if job is None:
            abort(404, message='Sorry, job {} not found'.format(job_id))
        if job.status == JobStatus.NOT_STARTED.value:
            return make_response(RequestStatus.FAILED,
                                 errors=['Cannot set state of not started job']
                                )
        if not job.fully_configured():
            return make_response(RequestStatus.FAILED,
                                 errors=['You must set all parameters '
                                         'before working with a job'])
        job.status = status.value
        db.session.commit()
        return make_response()
