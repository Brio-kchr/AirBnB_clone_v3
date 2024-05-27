#!/usr/bin/python3
"""New view for amenity objects that handles all default RESTFul API actions"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from os import name
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all():
    """retrieves the list of all amenity objects"""
    amenities = storage.all(Amenity)
    _list = []
    for amenity in amenities.values():
        _list.append(menity.to_dict())
    return jsonify(_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves an amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a new amenity"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    if 'name' not in response:
        abort(400, description='Missing name')
    new_amenity = Amenity(name=response['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity object"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
