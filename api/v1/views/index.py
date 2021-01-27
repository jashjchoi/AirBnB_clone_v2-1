#!/usr/bin/python3
"""Start the API in this file
Create a route on the object"""
from os import getenv
from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """route /status on app_views and return the status JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    obj_dict = {}
    for key, value in classes.items():
        obj_dict[key] = storage.count(value)
    return jsonify(obj_dict)

if __name__ == "__main__":
    pass
