from flask import Blueprint, jsonify, request
from api import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.models import Painting


paintings = Blueprint("paintings", __name__, url_prefix="/paintings")


@paintings.post("/")
@jwt_required()
def post_paintings():
    current_user = get_jwt_identity()
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    medium = request.get_json().get("medium", " ")
    genre = request.get_json().get("genre", " ")

    if len(title) < 2:
        return jsonify({"error": "painting title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where painting can be found cannot be blank"}), 400

    if len(medium) < 2:
        return jsonify({"error": "medium on which painting was made cannot be blank"}), 400

    painting = Painting(title=title, artist=artist, created=created,
                        object_place=object_place, medium=medium, genre=genre)

    db.session.add(painting)
    db.session.commit()

    return jsonify({
        "id": painting.id,
        "title": painting.title,
        "artist": painting.artist,
        "created": painting.created,
        "object_place": painting.object_place,
        "medium": painting.medium,
        "genre": painting.genre
    }), 201


@paintings.get("/")
def get_paintings():
    paintings = Painting.query.all()
    data = []

    for painting in paintings:
        data.append({
            "id": painting.id,
            "title": painting.title,
            "artist": painting.artist,
            "created": painting.created,
            "object_place": painting.object_place,
            "medium": painting.medium,
            "genre": painting.genre
        })
    return jsonify({"data": data}), 200


@paintings.get("/<int:id>")
def get_painting(id):
    painting = Painting.query.filter_by(id=id).first()

    if not painting:
        return jsonify({"error": "painting does not exist"}), 404
    else:
        return jsonify({
            "id": painting.id,
            "title": painting.title,
            "artist": painting.artist,
            "created": painting.created,
            "object_place": painting.object_place,
            "medium": painting.medium,
            "genre": painting.genre
        }), 200


@paintings.put("/<int:id>")
@jwt_required()
def update_painting(id):
    current_user = get_jwt_identity()
    painting = Painting.query.filter_by(id=id).first()

    if not painting:
        return jsonify({"error": "painting does not exist"}), 404
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    medium = request.get_json().get("medium", " ")
    genre = request.get_json().get("genre", " ")

    if len(title) < 2:
        return jsonify({"error": "painting title cannot be blank"}), 400

    if len(object_place) < 2:
        return jsonify({"error": "place where painting can be found cannot be blank"}), 400

    if len(medium) < 2:
        return jsonify({"error": "medium on which painting was made cannot be blank"}), 400

    painting.title = title
    painting.artist = artist
    painting.created = created
    painting.object_place = object_place
    painting.medium = medium
    painting.genre = genre

    db.session.commit()

    return jsonify({
        "id": painting.id,
        "title": painting.title,
        "artist": painting.artist,
        "created": painting.created,
        "object_place": painting.object_place,
        "medium": painting.medium,
        "genre": painting.genre
    }), 200


@paintings.delete("/<id>")
def delete_painting(id):
    painting = Painting.query.filter_by(id=id).first()

    if not painting:
        return jsonify({"error": "painting does not exist"}), 404

    db.session.delete(painting)
    db.session.commit()

    return jsonify({"message": "painting deleted"}), 204
