#!/usr/bin/python3
"""
This module handles all default RESTful API actions for Amenity objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Handle HTTP requests for amenity objects."""

    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        amenities_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities_list)

    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description="Not a JSON")
        name = req_data.get('name')
        if not name:
            abort(400, description="Missing name")
        amenity = Amenity(**req_data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """Handle HTTP requests for a specific amenity object."""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description="Not a JSON")
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
