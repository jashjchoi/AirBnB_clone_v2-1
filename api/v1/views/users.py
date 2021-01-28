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
    all_users = []
    for user in storage.all("User").values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_userid(user_id):
    """Display users by user_id"""
    all_users = storage.all("User").values()
    for user in all_users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete user by user_id"""
    u_id = storage.get(User, user_id)
    if u_id is None:
        abort(404)
    u_id.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new User"""
    req = request.get_json()
    if req is None:
        return make_response("Not a JSON", 400)
    if "email" not in req:
        return make_response("Missing email", 400)
    if "password" not in req:
        return make_response("Missing password", 400)
    new_user = User(**req)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a User object by user_id"""
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    req = request.get_json()
    if not req:
        return make_response("Not a JSON", 400)
    for key, val in req.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj_user, key, val)
    storage.save()
    return make_response(jsonify(obj_user.to_dict()), 200)
