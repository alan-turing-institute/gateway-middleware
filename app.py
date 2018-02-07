#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from connection import init_database, init_marshmallow

from routes import setup_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sg:sg@postgres/sg'

init_database(app)

init_marshmallow(app)

api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

setup_routes(api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
