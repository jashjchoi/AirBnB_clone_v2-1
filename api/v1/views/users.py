#!/usr/bin/python3
"""Create a route for users"""
from os import getenv
from models import storage
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Display all users"""
    obj_dict = []
    for obj in storage.all(User).values():
        obj_dict.append(obj.to_dict())
    return make_response(jsonify(obj_dict), 200)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_userid(user_id):
    """Display users by user_id"""
    u_id = storage.get(User, user_id)
    if u_id is not None:
        return make_response(jsonify(u_id.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete user by user_id"""
    u_id = storage.get(User, user_id)
    if user_id is not None:
        storage.delete(u_id)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new User"""
    req = request.get_json()
    if req is None:
        return make_response("Not a JSON", 400)
    if req.get('email') is None:
        return make_response("Missing email", 400)
    if req.get('password') is None:
        return make_response("Missing password", 400)
    else:
        new_user = User(**req)
        storage.new(new_user)
        storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a User object by user_id"""
    obj_user = storage.get(User, user_id)
    req = request.get_json()
    if obj_user is None:
        abort(404)
    if not req:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj_user, key, val)
    storage.save()
    return make_response(jsonify(obj_user.to_dict()), 200)
