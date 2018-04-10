"""
Make some fake routes for testing purposes
"""

from flask_restful import Resource

from tests.create_and_mint_case_using_stores import set_up_test_database


class TestData(Resource):
    """
    Class to be used for generating fake data
    """
    def post(self):
        """
        This just creates the default fake data
        """
        set_up_test_database()
