from flask_restful import Resource, Api, abort, reqparse

from sqlalchemy_classes import app, db, Case
from marshmallow_schema_classes import CaseSchema, CaseHeaderSchema

from webargs import fields
from webargs.flaskparser import use_args

api = Api(app)

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()

case_args = {
    'page': fields.Int(missing=1, validate= lambda p: p > 0),
    'per_page': fields.Int(missing=10, validate= lambda p: p > 0)
}

class CasesApi(Resource):
    @use_args(case_args)
    def get(self, args):
        return case_header_schema.dump(Case.query.paginate(args['page'], args['per_page'], False).items, many=True)


class CaseApi(Resource):
    def get(self, case_id: str):
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

api.add_resource(CasesApi, '/case')
api.add_resource(CaseApi, '/case/<case_id>')

if __name__ == '__main__':
    app.run(debug=True)
