#!/usr/bin/python3
""" Endpoint to handle all Review object requests"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
                '/api/v1/places/<place_id>/reviews',
                methods=['GET', 'POST']
)
def all_reviews(place_id):
    """ Handles all requests for reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        reviews = storage.all(Review)
        reviews_list = []
        for review in reviews.values():
            if review.place_id == place_id:
                reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    if request.method == "POST":
        new_review = request.get_json(silent=True)
        if new_review is None:
            return "Not a JSON", 400
        if "user_id" not in new_review.keys():
            return "Missing user_id", 400
        if "test" not in new_review.keys():
            return "Missing text", 400
        user = storage.get(User, reponse['user_id'])
        if user is None:
            abort(404)
        new_review["place_id"] = place.id
        new_review = Review(**new_review)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>',
                 methods=['DELETE', 'PUT', 'GET'])
def review(review_id):
    """ Endpoint does operations on a specific review"""
    review = storage.get(User, review_id)
    if review is None:
        abort(404)
    if request.method == "DELETE":
        review.delete()
        review.save()
        return jsonify({}), 200
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "PUT":
        edit_review = request.get_json(silent=True)
        if edit_review is None:
            return "Not a JSON", 400
        for key, value in edit_review.items():
            if key not in ["is", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
