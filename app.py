#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

import os
from time import sleep

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy.exc import OperationalError

from connection import init_database, init_marshmallow
from routes import set_up_routes

app = Flask(__name__)

logger = app.logger
config_mode = os.getenv("FLASK_CONFIGURATION", "development")
config_fname = "config.{}.json".format(config_mode.lower())
app.config.from_json(config_fname)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_loaded = False
while not db_loaded:
    try:
        db_loaded = True
        init_database(app)
    except OperationalError as e:
        db_loaded = False
        logger.error(e)
        sleep(3)

init_marshmallow(app)

api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

set_up_routes(app, api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
