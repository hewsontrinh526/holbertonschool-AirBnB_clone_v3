#!/usr/bin/python3
"""A file app.py that starts a Flask web application"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
import os



app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


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
