#!/usr/bin/python3
"""A file app.py that starts a Flask web application"""
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import make_response
from flask_cors import CORS
import os
import threading



app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host_name = os.getenv('HBNB_API_HOST', '0.0.0.0')
    host_port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host_name, port=host_port, threaded=True)
