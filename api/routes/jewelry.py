from flask import Blueprint, jsonify, request
from api import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.models import Jewelry


jewelries = Blueprint("jewelries", __name__, url_prefix="/jewelries")


@jewelries.post("/")
@jwt_required()
def post_jewelries():
    current_user = get_jwt_identity()
    title = request.get_json().get("title", " ")
    created = request.get_json().get("created", " ")
    country = request.get_json().get("country", " ")
    object_place = request.get_json().get("object_place", " ")
    medium = request.get_json().get("medium", " ")

    if len(title) < 2:
        return jsonify({"error": "jewelry title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where jewelry can be found cannot be blank"}), 400

    if len(country) < 2:
        return jsonify({"error": "country in which jewelry was found cannot be blank"}), 400

    if len(medium) < 2:
        return jsonify({"error": "material which was used to make jewelry cannot be blank"}), 400

    jewelry = Jewelry(title=title, country=country, created=created,
                        object_place=object_place, medium=medium)

    db.session.add(jewelry)
    db.session.commit()

    return jsonify({
        "id": jewelry.id,
        "title": jewelry.title,
        "country": jewelry.country,
        "created": jewelry.created,
        "object_place": jewelry.object_place,
        "medium": jewelry.medium,
    }), 201


@jewelries.get("/")
def get_jewelries():
    jewelries = Jewelry.query.all()
    data = []

    for jewelry in jewelries:
        data.append({
            "id": jewelry.id,
            "title": jewelry.title,
            "country": jewelry.country,
            "created": jewelry.created,
            "object_place": jewelry.object_place,
            "medium": jewelry.medium,

        })
    return jsonify({"data": data}), 200


@jewelries.get("/<int:id>")
def get_jewelry(id):
    jewelry = Jewelry.query.filter_by(id=id).first()

    if not jewelry:
        return jsonify({"error": "jewelry does not exist"}), 404
    else:
        return jsonify({
            "id": jewelry.id,
            "title": jewelry.title,
            "country": jewelry.country,
            "created": jewelry.created,
            "object_place": jewelry.object_place,
            "medium": jewelry.medium,
        }), 200


@jewelries.put("/<int:id>")
@jwt_required()
def update_jewelry(id):
    current_user = get_jwt_identity()
    jewelry = Jewelry.query.filter_by(id=id).first()

    if not jewelry:
        return jsonify({"error": "jewelry does not exist"}), 404
    title = request.get_json().get("title", " ")
    country = request.get_json().get("country", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    medium = request.get_json().get("medium", " ")

    if len(title) < 2:
        return jsonify({"error": "jewelry title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where jewelry can be found cannot be blank"}), 400

    if len(country) < 2:
        return jsonify({"error": "country in which jewelry was found cannot be blank"}), 400

    if len(medium) < 2:
        return jsonify({"error": "material which was used to make jewelry cannot be blank"}), 400

    jewelry.title = title
    jewelry.country = country
    jewelry.created = created
    jewelry.object_place = object_place
    jewelry.medium = medium

    db.session.commit()

    return jsonify({
            "id": jewelry.id,
            "title": jewelry.title,
            "country": jewelry.country,
            "created": jewelry.created,
            "object_place": jewelry.object_place,
            "medium": jewelry.medium,

        }), 200


@jewelries.delete("/<id>")
def delete_jewelry(id):
    jewelry = Jewelry.query.filter_by(id=id).first()

    if not jewelry:
        return jsonify({"error": "jewelry does not exist"}), 404

    db.session.delete(jewelry)
    db.session.commit()

    return jsonify({"message": "jewelry deleted"}), 204


