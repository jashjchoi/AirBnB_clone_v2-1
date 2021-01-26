#!/usr/bin/python3
"""Start the API in this file
Register the blueprint and execute the application"""
from os import getenv
from models import storage
from flask import Flask, Blueprint, jsonify, make_response
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close the storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
