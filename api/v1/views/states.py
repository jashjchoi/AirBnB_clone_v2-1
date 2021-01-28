#!/usr/bin/python3
""" State objects that handles all default RestFul API actions """
from models.state import State
from flask import abort, jsonify, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    list_states = []
    for state in storage.all("State").values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State by state_id"""
    st_id = storage.get(State, state_id)
    if not st_id:
        abort(404)
    return make_response(jsonify(st_id.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State by state_id"""
    state_id = storage.get(State, state_id)
    if state_id is not None:
        storage.delete(state_id)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new State"""
    if request.method == 'POST':
        list_states = []
        if not request.is_json:
            return make_response("Not a JSON", 400)
        list_states = State(**request.get_json())
        if 'name' not in list_states.to_dict().keys():
            return make_response("Missing name", 400)
        list_states.save()
        return make_response(jsonify(list_states.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Retrieves the list of all State objects """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response("Not a JSON"), 400)
    for k, v in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
