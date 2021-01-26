#!/usr/bin/python3
"""Start the API in this file. 
Create a route on the object"""
from os import getenv
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """route /status on app_views and return the status JSON"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass