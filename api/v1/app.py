#!/usr/bin/python3

"""
    This is the API server.
"""
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """
    handles the teardown method
    """
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """Returns 404 not found error message"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)

