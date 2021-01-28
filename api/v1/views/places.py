#!/usr/bin/python3
"""Create a route for places"""
from os import getenv
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Display list of places by a given city"""
    c_id = storage.get(City, city_id)
    if c_id is not None:
        return jsonify([place.to_dict() for place in c_id.places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Display the place by place_id"""
    p_id = storage.get(Place, place_id)
    if p_id is not None:
        return jsonify(p_id.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['POST'],
                 strict_slashes=False)
    """ Updates a place """
    if not place
        abort(404)
    if not request.get_json()
        abort(400, description="Not a JSON")
    for k, v in request.json.items().items()
        if k not in ['id', 'user_id','city_id', 'created_at', 'updated_at']:
             setattr(place, key, value)
    storage.save()
    return (place.to_dict(), 200)
