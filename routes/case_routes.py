"""
Defintions of routes for the app
"""

from flask_restful import Resource, abort

from connection.models import Case
from connection.schemas import CaseSchema, CaseHeaderSchema

from webargs.flaskparser import use_kwargs

from .common_args import pagination_args

case_schema = CaseSchema()
case_header_schema = CaseHeaderSchema()


class CasesApi(Resource):
    """
    Api for the list of all cases
    """
    @use_kwargs(pagination_args)
    def get(self, page, per_page):
        """
        Get all the cases that are in the requested range
        """
        return case_header_schema.dump(Case.query.paginate(page, per_page,
                                                           False).items,
                                       many=True)


class CaseApi(Resource):
    """
    End point for dealing with a specific case
    """
    def get(self, case_id: str):
        """
        Get all the details for a specific case
        """
        try:
            case_id = int(case_id)
        except ValueError as e:
            print(e)
            abort(404, message='Sorry no such case {}'. format(case_id))
        case = Case.query.get(case_id)
        if case is not None:
            return case_schema.dump(case)
        else:
            abort(404, message='Sorry, case {} not found'.format(case_id))
