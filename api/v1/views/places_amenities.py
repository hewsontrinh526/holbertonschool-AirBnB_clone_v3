#!/usr/bin/python3
"""
A new view for the link between Place objects and Amenity objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_place_amenities_list(place_id):
    """Retrieves a list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if storage_type == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([storage.get(Amenity, amenity_id).to_dict
                        for amenity_id in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if storage_type == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if storage_type == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
