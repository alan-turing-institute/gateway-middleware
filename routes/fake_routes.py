"""
Make some fake routes for testing purposes
"""

from flask_restful import Resource
from tests.create_and_mint_case_using_stores import set_up_test_database
from tests.create_cavity_case import set_up_cavity_testdata
from tests.create_damBreak_case import set_up_dambreak_testdata


class TestData(Resource):
    """
    Class to be used for generating fake data
    """

    def post(self):
        """
        Create the default fake data
        """
        # set_up_test_database()
        set_up_dambreak_testdata()
        set_up_cavity_testdata()
