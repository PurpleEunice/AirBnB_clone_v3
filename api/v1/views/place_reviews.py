#!/usr/bin/python3
"""
Page handlr for places_reviews
"""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_post_reviews_by_place(place_id):
    """
    Retrieve and create reviews for a given place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.is_json:
            return {"error": "Not a JSON"}, 400

        json_data = request.get_json()
        user_id = json_data.get("user_id")
        if user_id is None:
            return {"error": "Missing user_id"}, 400

        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        if "text" not in json_data:
            return {"error": "Missing text"}, 400

        new_review = Review(place_id=place_id, **json_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_update_review(review_id):
    """
    Retrieve, delete, or update a review by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            return {"error": "Not a JSON"}, 400

        json_data = request.get_json()
        for key, value in json_data.items():
            if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200

    # fallback case (should never be reached)
    abort(500)
