#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

from flask import Flask
from flask_restful import Api

from connection import init_database, init_marshmallow

from routes import setup_routes, CasesApi, CaseApi

from .create_and_mint_case_using_stores import set_up_test_database

from pytest import fixture

from .decorators import request_context


@fixture(scope="module")
def app():
    """
    Setup the flask app context I hope
    """
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.testing = True

    init_database(app)
    init_marshmallow(app)

    api = Api(app)

    setup_routes(api)
    with app.app_context():
        set_up_test_database()
    return app


def test_something(app):
    """
    Test that a basic query of gets lots of cases
    """
    with app.app_context():
        with app.test_request_context('a', method="GET"):
            result = CaseApi().dispatch_request(1)
            print(result.data)


@request_context("/case?per_page=1", method="GET")
def test_1_per_page(app):
    print(app)
    result = CasesApi().dispatch_request()
    assert(len(result.data) == 1)


@request_context("/case", method="GET")
def test_per_page(app):
    print(app)
    result = CasesApi().dispatch_request()
    assert(len(result.data) == 3)
