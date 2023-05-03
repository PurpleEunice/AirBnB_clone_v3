#!/usr/bin/python3
"""
handles the states page
"""
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """
    Retrieves a list of all stte obects
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return {"error": "Not a JSON"}, 400
        if "name" not in data:
            return {"error": "Missing name"}, 400
        new_state = State(**data)
        new_state.save()
        return new_state.to_dict(), 201
    if request.method == 'GET':
        states = [s.to_dict() for s in storage.all("State").values()]
        return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_state(state_id):
    """
        specific id querrying
    """
    state_obj = storage.get(State, state_id)
    if (state_obj):
        if request.method == 'DELETE':
            state_obj.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return {"error": "Not a JSON"}, 400
            for key, value in data.items():
                if key not in ["created_at", "id", "updated_at"]:
                    setattr(state_obj, key, value)
            state_obj.save()
        return state_obj.to_dict()
    abort(404)
