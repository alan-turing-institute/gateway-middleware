#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from connection import init_database, init_marshmallow

from routes import setup_routes

import connection.constants as const

from json import load

app = Flask(__name__)

with open('config.json') as json:
    args = load(json)
    app.config['SQLALCHEMY_DATABASE_URI'] = args['database_url']
    const.JOB_MANAGER_URL = args['job_manager_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app)

init_marshmallow(app)

api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

setup_routes(api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
