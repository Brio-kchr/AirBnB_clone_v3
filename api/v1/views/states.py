#!/usr/bin/python3
"""New view for State objects that handles all default RESTFul API actions"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from os import name
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all():
    """retrieves the list of all State objects"""
    states = storage.all(State)
    _list = []
    for state in states.values():
        _list.append(state.to_dict())
    return jsonify(_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves a state object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    if 'name' not in response:
        abort(400, description='Missing name')
    new_state = State(name=response['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
