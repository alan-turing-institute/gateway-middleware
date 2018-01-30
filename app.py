from flask_restful import Resource, Api, abort, reqparse
from flask_cors import CORS 

from sqlalchemy.exc import IntegrityError

from sqlalchemy_classes import app, db, Case, MintedCase, MintedValue
from marshmallow_schema_classes import CaseSchema, CaseHeaderSchema, JobHeaderSchema, JobSchema

from webargs import fields, missing
from webargs.flaskparser import use_kwargs

api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()
job_header_schema = JobHeaderSchema()
job_schema = JobSchema()

pagination_args = {
    'page': fields.Int(missing=1, validate= lambda p: p > 0),
    'per_page': fields.Int(missing=10, validate= lambda p: p > 0)
}

job_args = {
    'case_id': fields.Int(required=True),
    'author': fields.Str(required=True),
    'name': fields.Str(required=True)
}

job_argument_args = {
    'name': fields.Str(required=True),
    'value': fields.Str(required=True)
}

job_patch_args = {
    'name': fields.Str(),
    'values': fields.List(fields.Nested(job_argument_args))
}

class CasesApi(Resource):
    @use_kwargs(pagination_args)
    def get(self, page, per_page):
        """
        Get all the cases that are in the requested range
        """        
        return case_header_schema.dump(Case.query.paginate(page, per_page, False).items, many=True)


class CaseApi(Resource):
    def get(self, case_id: str):
        """
        Get all the details for a specific case
        """
        try:
            case_id = int(case_id)
        except ValueError as e:
            print(e)
            abort(404, message= "Sorry no such case {}". format(case_id))
        case = Case.query.get(case_id)
        if case is not None:
            return case_schema.dump(case)
        else:
            abort(404, message="Sorry, case {} not found".format(case_id))


class JobsApi(Resource):
    @use_kwargs(job_args, locations=('json',))
    def post(self, case_id, name, author):
        """
        Create a new job based on a case
        """
        try:
            new_minted_case = MintedCase(mintedcase_name=name, user=author, case_id=case_id)
            db.session.add(new_minted_case)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            abort(404, message="Sorry, these parameters have already been used")
        return {'mintedcase_id': new_minted_case.mintedcase_id}

    @use_kwargs(pagination_args)
    def get(self, page, per_page):
        """
        Get all the jobs that are in the requested range
        """        
        return job_header_schema.dump(MintedCase.query.paginate(page, per_page, False).items, many=True)

class JobApi(Resource):
    def get(self, job_id):
        """
        Get the specified job
        """        
        try:
            job_id = int(job_id)
        except ValueError as e:
            print(e)
            abort(404, message= "Sorry no such job {}". format(job_id))
        job = MintedCase.query.get(job_id)
        if job is not None:
            return job_schema.dump(job)
        else:
            abort(404, message="Sorry, job {} not found".format(job_id))

    @use_kwargs(job_patch_args)
    def patch(self, job_id, name, values):
        """
        Update the given details for this job
        """
        if name is missing and values is missing:
            # You don't actually need to change anything
            return { 'status': 'success'}
        job = MintedCase.query.get(job_id)
        if job is None:
            abort(404, message="Sorry, job {} not found".format(job_id))
        if name is not missing:
            job.mintedcase_name = name
        if values is not missing:
            for value in job.values:
                db.session.delete(value)
            for value in values:
                new_minted_value = MintedValue(name= value['name'], value= value['value'], parent_mintedcase=job)
                job.values.append(new_minted_value)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            abort(404, message="Sorry. Failed to commit your request")
        return { 'status': 'success'}


api.add_resource(CasesApi, '/case')
api.add_resource(CaseApi, '/case/<case_id>')
api.add_resource(JobsApi, '/job')
api.add_resource(JobApi, '/job/<job_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
