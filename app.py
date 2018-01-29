from flask_restful import Resource, Api, abort

from sqlalchemy_classes import app, db, Case
from marshmallow_schema_classes import CaseSchema, CaseHeaderSchema

api = Api(app)

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()

class CasesApi(Resource):
    def get(self):
        return case_header_schema.dump(Case.query.all(), many=True)


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
