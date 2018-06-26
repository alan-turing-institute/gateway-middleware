#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from connection import init_database, init_marshmallow
from routes import set_up_routes

app = Flask(__name__)

config_mode = os.getenv('FLASK_CONFIGURATION', 'development')
config_fname = 'config.{}.json'.format(config_mode.lower())
app.config.from_json(config_fname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app)

init_marshmallow(app)

api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

set_up_routes(app, api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
