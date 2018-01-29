from flask_restful import Resource, Api, abort, reqparse

from sqlalchemy_classes import app, db, Case
from marshmallow_schema_classes import CaseSchema, CaseHeaderSchema

from webargs import fields
from webargs.flaskparser import use_kwargs

api = Api(app)

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()

case_args = {
    'page': fields.Int(missing=1, validate= lambda p: p > 0),
    'per_page': fields.Int(missing=10, validate= lambda p: p > 0)
}

job_args = {
    'case_id': fields.Int(required=True)
}

class CasesApi(Resource):
    @use_kwargs(case_args)
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


class JobApi(Resource):
    @use_kwargs(job_args, locations=('headers',))
    def post(self, case_id):
        """
        Create a new job based on a case
        """
        return { 'case': case_id }


api.add_resource(CasesApi, '/case')
api.add_resource(CaseApi, '/case/<case_id>')
api.add_resource(JobApi, '/job')

if __name__ == '__main__':
    app.run(debug=True)
