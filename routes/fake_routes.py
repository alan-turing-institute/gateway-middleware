"""
Make some fake routes for testing purposes
"""
from flask_restful import Resource

from tests.create_cavity_case import set_up_cavity_testdata
from tests.create_damBreak_case import set_up_dambreak_testdata

from connection.models import db, Case


class TestData(Resource):
    """
    Class to be used for generating fake data
    """

    def post(self):
        """
        Create the default fake data
        """
        # set_up_test_database()
        messages = []
        errors = []
        message = set_up_dambreak_testdata()
        messages.append(message)

        message = set_up_cavity_testdata()
        messages.append(message)

        return {"status": "success", "messages": messages, "errors": errors}

    # def delete(self):
    #     """
    #     Delete all data
    #     """
    #     messages = []
    #     errors = []

    #     db.session.query(Case).delete()
    #     db.session.commit()

    #     messages.append("Emptied case table.")

    #     return {"status": "success", "messages": messages, "errors": errors}

