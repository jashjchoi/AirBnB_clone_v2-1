#!/usr/bin/python3
"""Start the API in this file
Register the blueprint and execute the application"""
from os import getenv
from models import storage
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found_404(err):
    """returns page not found 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
