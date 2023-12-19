#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON response with status OK"""
    return jsonify({"status": "OK"})
