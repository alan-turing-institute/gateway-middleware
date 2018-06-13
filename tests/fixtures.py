"""
Helpful fixtures for testing
"""
from uuid import uuid4

from flask import Flask
from flask_restful import Api
from pytest import fixture

from connection import init_database, init_marshmallow
from connection.models import db, Job, JobParameter, JobStatus
from routes import setup_routes
from .create_and_mint_case_using_stores import set_up_test_database


@fixture(scope='session')
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


@fixture(scope='session')
def test_job_id(demo_app):
    """
    Create a test job with a known job_id and add it to the db
    """
    job_id = str(uuid4())
    job = Job(id=job_id, case_id='3',
              name='bob', user='bob2')
    job.description = 'this is a test job'
    length = JobParameter(name='length', value='3')
    width = JobParameter(name='width', value='3')
    f1_density = JobParameter(name='Fluid1_density', value='1000')
    f2_density = JobParameter(name='Fluid2_density', value='1000')
    f1_viscosity = JobParameter(name='Fluid1_viscosity', value='1')
    f2_viscosity = JobParameter(name='Fluid2_viscosity', value='1')
    job.values.append(length)
    job.values.append(width)
    job.values.append(f1_density)
    job.values.append(f2_density)
    job.values.append(f1_viscosity)
    job.values.append(f2_viscosity)
    job.status = JobStatus.NOT_STARTED.value
    with demo_app.app_context():
        session = db.session
        session.add(job)
        session.commit()
    return job_id


@fixture(scope='session')
def test_job_id_no_values(demo_app):
    """
    Create a test job with a known job_id but not values set,
    and add it to the db
    """
    job_id = str(uuid4())
    job = Job(id=job_id, case_id='1',
              name='bob_no_val', user='bob2')
    job.description = 'this is another test job'
    job.status = JobStatus.NOT_STARTED.value
    with demo_app.app_context():
        session = db.session
        session.add(job)
        session.commit()
    return job_id
