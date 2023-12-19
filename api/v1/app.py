#!/usr/bin/python3
"""A file app.py that starts a Flask web application"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv


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
    app_host = getenv("HBNB_API_HOST")
    app_port = getenv("HBNB_API_PORT")
    if app_host is None:
        app_host = "0.0.0.0"
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=app_port)
