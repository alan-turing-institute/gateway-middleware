#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

from flask import Flask
from flask_restful import Api

from connection import init_database, init_marshmallow

from routes import setup_routes, CasesApi, CaseApi

from create_and_mint_case_using_stores import set_up_test_database


def test_something():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.testing = True

    init_database(app)

    init_marshmallow(app)

    api = Api(app)

    setup_routes(api)

    with app.app_context():
        set_up_test_database()
        with app.test_request_context('a', method="GET"):
            print(CaseApi().dispatch_request(1))  # Manually put in the case id

        with app.test_request_context("/case", method="GET"):
            # This fails because it cannot generate the self URL in the links section
            print(CasesApi().dispatch_request())
