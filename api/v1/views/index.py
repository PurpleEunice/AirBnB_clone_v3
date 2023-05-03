#!/usr/bin/python3

"""
    The index file serves index page
"""
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    """   
    route at /status
    This will display the status of our app
    """
    return {"status": "OK"}

@app_views.route('/stats')
def get_stats():
    """
    calls the method count on storage
    """
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    return {classname: storage.count(obj) for classname, obj in classes.items()}
