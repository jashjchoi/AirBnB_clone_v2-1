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
def all_places_by_city(city_id):
    """Display list of places by a given city"""
    c_id = storage.get(City, city_id)
    if c_id is None:
        abort(404)
    list_places = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Display the place by place_id"""
    p_id = storage.get(Place, place_id)
    if p_id is not None:
        return jsonify(p_id.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """delete a Place by place_id"""
    p_id = storage.get(Place, place_id)
    if p_id is None:
        abort(404)
    p_id.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creates a new Place in the given city"""
    c_id = storage.get(City, city_id)
    if not c_id:
        abort(404)
    req = request.get_json()
    if not req:
        return make_response("Not a JSON", 400)
    if "user_id" not in req.keys():
        return make_response("Missing user_id", 400)
    u_id = storage.get(User, req['user_id'])
    if not u_id:
        abort(404)
    if "name" not in req:
        return make_response("Missing name", 400)
    new_place = Place(**req)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req = request.get_json()
    if not req:
        return make_response("Not a JSON", 400)
    for k, v in req.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
