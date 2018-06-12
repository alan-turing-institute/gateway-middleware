"""
Helpful fixtures for testing
"""
from uuid import uuid4

from flask import Flask
from flask_restful import Api
from pytest import fixture

from connection import init_database, init_marshmallow
from connection.models import Job
from routes import setup_routes
from .create_and_mint_case_using_stores import set_up_test_database


@fixture(scope='module')
def demo_app():
    """
    Setup the flask app context I hope
    """
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.testing = True

    init_database(app)
    init_marshmallow(app)

    api = Api(app)

    setup_routes(app, api)
    with app.app_context():
        set_up_test_database()
    return app

@fixture(scope='module')
def test_job():
    """
    Create a test job with a known job_id
    """
    job = Job(id=str(uuid4()), name="bob")
    return job
