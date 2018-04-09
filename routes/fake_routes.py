"""
Make some fake routes for testing purposes
"""

from flask_restful import Resource

from tests.create_and_mint_case_using_stores import set_up_test_database

from tests.openfoam_test_data import upload_dambreak_test

class TestData(Resource):
    """
    Class to be used for generating fake data
    """
    def post(self,test_id):
        """
        This just creates the default fake data
        """
        if test_id == 0:
            set_up_test_database()
        else:
            upload_dambreak_test()
