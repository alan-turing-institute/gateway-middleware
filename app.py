from flask_restful import Resource, Api, abort, reqparse

from sqlalchemy_classes import app, db, Case, MintedCase
from marshmallow_schema_classes import CaseSchema, CaseHeaderSchema, JobHeaderSchema

from webargs import fields
from webargs.flaskparser import use_kwargs

api = Api(app)

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()
job_header_schema = JobHeaderSchema()

pagination_args = {
    'page': fields.Int(missing=1, validate= lambda p: p > 0),
    'per_page': fields.Int(missing=10, validate= lambda p: p > 0)
}

job_args = {
    'case_id': fields.Int(required=True),
    'author': fields.Str(required=True),
    'name': fields.Str(required=True)
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
        new_minted_case = MintedCase(mintedcase_name=name, user=author, case_id=case_id)
        db.session.add(new_minted_case)
        db.session.commit()
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
        return { 'job_id': job_id }


api.add_resource(CasesApi, '/case')
api.add_resource(CaseApi, '/case/<case_id>')
api.add_resource(JobsApi, '/job')
api.add_resource(JobApi, '/job/<job_id>')

if __name__ == '__main__':
    app.run(debug=True)
