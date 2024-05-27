#!/usr/bin/python3
""" Endpoint to handle all User object requests"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route(
	'/api/v1/users', methods=['GET', 'POST'])
@app_views.route(
	'/api/v1/users/', methods=['GET', 'POST'])
def all_users():
	""" handles requests for users from storage"""
	if request.method == "GET":
		users = storage.all(User)
		list_users = []
		for user in users.values():
			list_users.append(user.to_dict())
		return jsonify(list_users)
	if request.method == "POST":
		new_user = request.get_json(silent=True)
		if new_user is None:
			return "Not a JSON", 400
		if "email" not in new_user.keys():
			return "Missing email", 400
		if "password" not in new_user.keys():
			return "Missing password", 400
		new_user = User(**new_user)
		new_user.save()
		return jsonify(new_user.to_dict()), 201

@app_views.route('/api/v1/users/<user_id>', methods=['DELETE', 'PUT', 'GET'])
def query_user(user_id):
	""" Endpoint does operations on a specific user"""
	user = storage.get(User, user_id)
	if user is None:
		abort(404)
	if request.method == "DELETE":
		user.delete()
		storage.save()
		return jsonify({}), 200
	if request.method == "GET":
		return jsonify(user.to_dict())
	if request.method == "PUT":
		edit_user = request.get_json(silent=True)
		if edit_user is None:
			return "Not a JSON", 400
		for key, value in edit_user.items():
			if (key != "id") and
			   (key != "created_at") and
			   (key != "updated_at") and
			   (key != "email"):
				setattr(user, key, value)
		user.save()
		return jsonify(user.to_dict())
