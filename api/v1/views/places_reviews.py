#!/usr/bin/python3
""" Review objects that handle all default RestFul API actions """
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ All Reviews of a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Review of a specific id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Create a new Review """
    p_id = storage.get(Place, place_id)
    if p_id is None:
        abort(404)
    req = request.get_json()
    if not req:
        return make_response("Not a JSON", 400)
    u_id = storage.get(User, req['user_id'])
    if not u_id:
        abort(404)
    if "user_id" not in req.keys():
        return make_response("Missing user_id", 400)
    if "text" not in req:
        return make_response("Missing text", 400)
    new_review = Review(**req)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Update a review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
