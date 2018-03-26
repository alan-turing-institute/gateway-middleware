"""
Defintions of routes for the app
"""

from flask_restful import Resource, abort

from sqlalchemy.exc import IntegrityError

from connection.models import Job, db
from connection.schemas import JobHeaderSchema, JobSchema
from connection.api_schemas import JobArgs, JobPatchArgs, PaginationArgs
from connection.constants import JobStatus, RequestStatus, JOB_MANAGER_URL

from webargs import missing
from webargs.flaskparser import use_kwargs

import requests

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
            abort(404, message='Sorry no such job {}'. format(job_id))
        job = Job.query.get(job_id)
        if job is not None:
            return job_schema.dump(job)
        else:
            abort(404, message='Sorry, job {} not found'.format(job_id))

    @use_kwargs(JobPatchArgs())
    def patch(self, job_id, name, values):
        """
        Update the given details for this job
        """
        changed = []
        error_log = []
        status = RequestStatus.SUCCESS.value
        if name is missing and values is missing:
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
            return {
                'status': RequestStatus.FAILED.value,
                'errors': ['Job already started']
            }
        if not job.fully_configured():
            return {
                'status': RequestStatus.FAILED.value,
                'errors': ['You must set all parameters before running a job']
            }
        params = {
            'fields_to_patch': job.field_list(),
            'scripts': job.script_list()
        }
        response = requests.post('{}/{}/start'.format(JOB_MANAGER_URL, job_id),
                                 params)
        if response.status_code != 200:
            return {
                    'status': RequestStatus.FAILED.value,
                    'errors': ['Job Managed returned HTTP ' +
                               response.status_code]
                   }
        result = response.json
        # TODO: Handle non http errors - but they haven't been implemented
        job.status = JobStatus.QUEUED.value
        db.session.commit()
        return {'status': RequestStatus.SUCCESS.value}
