#!/usr/bin/python3
"""New view for place objects that handles all default RESTFul API actions"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from os import name
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places():
    """retrieves the list of all place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    _list = []
    for place in places.values():
        _list.append(place.to_dict())
    return jsonify(_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves a place object by id"""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place object"""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place():
    """creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in response:
        abort(400, description='Missing user_id')
    if 'name' not in response:
        abort(400, description='Missing name')
    user = storage.get(User, response['user_id'])
    if user is None:
        abort(404)
    new_place = Place(**response)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place object"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
