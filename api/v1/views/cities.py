#!/usr/bin/python3
""" View for accessing City objects"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def all_state_cities(state_id):
	""" handles requests for cities in a state from storage"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	all_cities = storage.all(City)
	list_city = []
	for city in all_cities.values():
		if city.state_id == state.id:
			list_city.append(city.to_dict())
	return jsonify(city_list)

@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
	"""Creates a new City object."""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	new_city = request.get_json(silent=True)
	if new_city is None:
		return "Not a JSON", 400
	if "name" not in new_city.keys():
		return "Missing name", 400
	new_city["state_id"] = state.id
	new_city = City(**new_city)
	new-city.save()
	return jsonify(new_city.to_dict()), 201

@app_views.route('GET /api/v1/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city(sity_id):
	"""Retrieves a City object."""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	if request.method == "GET":
		return jsonify(city.to_dict())
	if request.method == "DELETE":
		city.delete()
		storage.save()
		return jsonify({})
	if request.method == "PUT":
		edit_city = request.get_json(silent=True)
		if edit_city is None:
			return "Not a JSON", 400
		for key, value in edit_city.items():
			if (key != "id") and (key != "created_at") and (key != "updated_at"):
				setattr(city, key, value)
		city.save()
		return jsonify(city.to_dict())
