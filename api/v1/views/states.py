#!/usr/bin/python3
""" State objects that handles all default RestFul API actions """
from models.state import State
from flask import abort, jsonify, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    if request.method == "GET":
        list_states = []
        for state in storage.all("State").values():
            list_states.append(state.to_dict())
            return jsonify(list_states)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Retrieves the list of all State objects """
    if request.method == 'POST':
        list_states = []
        if not request.is_json:
            abort(400, 'Not a JSON')
        list_states = State(**request.get_json())
        if 'name' not in list_states.to_dict().keys():
                abort(400, 'Missing name'
        list_states.save()
            return (list_states.to_dict(), 201)

