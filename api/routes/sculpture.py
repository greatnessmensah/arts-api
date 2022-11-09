from flask import Blueprint, jsonify, request
from api import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.models import Sculpture


sculptures = Blueprint("sculptures", __name__, url_prefix="/sculptures")


@sculptures.post("/")
@jwt_required()
def post_sculptures():
    current_user = get_jwt_identity()
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    material = request.get_json().get("material", " ")

    if len(title) < 2:
        return jsonify({"error": "sculpture title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where sculpture can be found cannot be blank"}), 400

    if len(material) < 2:
        return jsonify({"error": "material which was used to make sculpture cannot be blank"}), 400

    sculpture = Sculpture(title=title, artist=artist, created=created,
                          object_place=object_place, material=material)

    db.session.add(sculpture)
    db.session.commit()

    return jsonify({
        "id": sculpture.id,
        "title": sculpture.title,
        "artist": sculpture.artist,
        "created": sculpture.created,
        "object_place": sculpture.object_place,
        "material": sculpture.material,
    }), 201


@sculptures.get("/")
def get_sculptures():
    sculptures = Sculpture.query.all()
    data = []

    for sculpture in sculptures:
        data.append({
            "id": sculpture.id,
            "title": sculpture.title,
            "artist": sculpture.artist,
            "created": sculpture.created,
            "object_place": sculpture.object_place,
            "material": sculpture.material,
        })
    return jsonify({"data": data}), 200


@sculptures.get("/<int:id>")
def get_sculpture(id):
    sculpture = Sculpture.query.filter_by(id=id).first()

    if not sculpture:
        return jsonify({"error": "sculpture does not exist"}), 404
    else:
        return jsonify({
            "id": sculpture.id,
            "title": sculpture.title,
            "artist": sculpture.artist,
            "created": sculpture.created,
            "object_place": sculpture.object_place,
            "material": sculpture.material,
        }), 200


@sculptures.put("/<int:id>")
@jwt_required()
def update_sculpture(id):
    current_user = get_jwt_identity()
    sculpture = Sculpture.query.filter_by(id=id).first()

    if not sculpture:
        return jsonify({"error": "sculpture does not exist"}), 404
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    material = request.get_json().get("material", " ")

    if len(title) < 2:
        return jsonify({"error": "sculpture title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where sculpture can be found cannot be blank"}), 400

    if len(medium) < 2:
        return jsonify({"error": "material which was used to make sculpture cannot be blank"}), 400

    sculpture.title = title
    sculpture.artist = artist
    sculpture.created = created
    sculpture.object_place = object_place
    sculpture.material = material

    db.session.commit()

    return jsonify({
        "id": sculpture.id,
        "title": sculpture.title,
        "artist": sculpture.artist,
        "created": sculpture.created,
        "object_place": sculpture.object_place,
        "material": sculpture.material,
    }), 200


@sculptures.delete("/<id>")
def delete_sculpture(id):
    sculpture = Sculpture.query.filter_by(id=id).first()

    if not sculpture:
        return jsonify({"error": "sculpture does not exist"}), 404

    db.session.delete(sculpture)
    db.session.commit()

    return jsonify({"message": "sculpture deleted"}), 204
