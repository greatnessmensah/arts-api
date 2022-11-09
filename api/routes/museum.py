from flask import Blueprint, jsonify, request
from api import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.models import Museum, Painting, Sculpture, Jewelry


museums = Blueprint("museums", __name__, url_prefix="/museums")


@museums.post("/")
@jwt_required()
def post_museums():
    current_user = get_jwt_identity()
    name = request.get_json().get("name", " ")
    country = request.get_json().get("country", " ")
    city = request.get_json().get("city", " ")
    established = request.get_json().get("established", " ")

    if len(name) < 2:
        return jsonify({"error": "museum name cannot be blank"}), 400

    if len(country) < 2:
        return jsonify({"error": "museum country cannot be blank"}), 400

    if len(city) < 2:
        return jsonify({"error": "museum city cannot be blank"}), 400

    museum = Museum(name=name, country=country,
                    city=city, established=established)

    db.session.add(museum)
    db.session.commit()

    return jsonify({
        "id": museum.id,
        "name": museum.name,
        "country": museum.country,
        "city": museum.city,
        "established": museum.established
    }), 201


@museums.get("/<int:id>")
def get_painting(id):
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    else:
        paintings = Painting.query.filter_by(place=museum).all()
        paint = []
        sculptures = Sculpture.query.filter_by(place=museum).all()
        sculp = []
        jewelries = Jewelry.query.filter_by(place=museum).all()
        jewel = []

        for painting in paintings:
            paint.append({
                "id": painting.id,
                "title": painting.title,
                "artist": painting.artist,
                "created": painting.created,
                "object_place": painting.object_place,
                "medium": painting.medium,
                "genre": painting.genre
            })
        for sculpture in sculptures:
            sculp.append({
                "id": sculpture.id,
                "title": sculpture.title,
                "artist": sculpture.artist,
                "created": sculpture.created,
                "object_place": sculpture.object_place,
                "material": sculpture.material,
            })
        for jewelry in jewelries:
            jewel.append({
                "id": jewelry.id,
                "title": jewelry.title,
                "country": jewelry.country,
                "created": jewelry.created,
                "object_place": jewelry.object_place,
                "medium": jewelry.medium,
            })
    return jsonify({
        "id": museum.id,
        "name": museum.name,
        "country": museum.country,
        "city": museum.city,
        "established": museum.established,
        "paintings": paint,
        "sculptures": sculp,
        "jewelries": jewel
    }), 200


@museums.put("/<int:id>")
@jwt_required()
def update_painting(id):
    current_user = get_jwt_identity()
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    name = request.get_json().get("name", " ")
    country = request.get_json().get("country", " ")
    city = request.get_json().get("city", " ")
    established = request.get_json().get("established", " ")

    if len(name) < 2:
        return jsonify({"error": "museum name cannot be blank"}), 400

    if len(country) < 2:
        return jsonify({"error": "museum country cannot be blank"}), 400

    if len(city) < 2:
        return jsonify({"error": "museum city cannot be blank"}), 400

    museum.name = name
    museum.country = country
    museum.city = city
    museum.established = established

    db.session.commit()

    return jsonify({
        "id": museum.id,
        "name": museum.name,
        "country": museum.country,
        "city": museum.city,
        "established": museum.established,
    }), 200


@museums.delete("/<id>")
def delete_painting(id):
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404

    db.session.delete(museum)
    db.session.commit()

    return jsonify({"message": "museum deleted"}), 204


@museums.post("/<int:id>/paintings/")
@jwt_required()
def post_museum_painting(id):
    current_user = get_jwt_identity()
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    medium = request.get_json().get("medium", " ")
    genre = request.get_json().get("genre", " ")

    painting = Painting(title=title, artist=artist, created=created,
                        object_place=object_place, medium=medium, genre=genre, place=museum)

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


@museums.get("<int:id>/paintings")
def get_all_museum_paintings(id):
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    paintings = Painting.query.filter_by(place=museum).all()
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


@museums.get("/<int:m_id>/paintings/<int:p_id>")
def get_museum_painting(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    painting = Painting.query.filter_by(place=museum, id=p_id).first()
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


@museums.delete("/<int:m_id>/paintings/<int:p_id>")
def delete_museum_painting(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    painting = Painting.query.filter_by(place=museum, id=p_id).first()
    if not painting:
        return jsonify({"error": "painting does not exist"}), 404

    db.session.delete(painting)
    db.session.commit()

    return jsonify({"message": "painting deleted"}), 204


@museums.post("/<int:id>/sculptures/")
@jwt_required()
def post_museum_sculpture(id):
    current_user = get_jwt_identity()
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    title = request.get_json().get("title", " ")
    artist = request.get_json().get("artist", " ")
    created = request.get_json().get("created", " ")
    object_place = request.get_json().get("object_place", " ")
    material = request.get_json().get("material", " ")

    sculpture = Sculpture(title=title, artist=artist, created=created,
                          object_place=object_place, material=material, place=museum)

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


@museums.get("<int:id>/sculptures")
def get_all_museum_sculptures(id):
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    sculptures = Sculpture.query.filter_by(place=museum).all()
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


@museums.get("/<int:m_id>/sculptures/<int:p_id>")
def get_museum_sculpture(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    sculpture = Sculpture.query.filter_by(place=museum, id=p_id).first()
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
        }), 201


@museums.delete("/<int:m_id>/sculptures/<int:p_id>")
def delete_museum_sculpture(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    sculpture = Sculpture.query.filter_by(place=museum, id=p_id).first()
    if not sculpture:
        return jsonify({"error": "sculpture does not exist"}), 404

    db.session.delete(sculpture)
    db.session.commit()

    return jsonify({"message": "sculpture deleted"}), 204


@museums.post("/<int:id>/jewelries/")
@jwt_required()
def post_museum_jewelry(id):
    current_user = get_jwt_identity()
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
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
                      object_place=object_place, medium=medium, place=museum)

    db.session.add(jewelry)
    db.session.commit()

    return jsonify({
        "id": jewelry.id,
        "title": jewelry.title,
        "country": jewelry.country,
        "created": jewelry.created,
        "object_place": jewelry.object_place,
        "medium": jewelry.medium
    }), 201


@museums.get("<int:id>/jewelries")
def get_all_museum_jewelries(id):
    museum = Museum.query.filter_by(id=id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    jewelries = Jewelry.query.filter_by(place=museum).all()
    data = []

    for jewelry in jewelries:
        data.append({
            "id": jewelry.id,
            "title": jewelry.title,
            "country": jewelry.country,
            "created": jewelry.created,
            "object_place": jewelry.object_place,
            "medium": jewelry.medium
        })
    return jsonify({"data": data}), 200


@museums.get("/<int:m_id>/jewelries/<int:p_id>")
def get_museum_jewelry(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    jewelry = Jewelry.query.filter_by(place=museum, id=p_id).first()
    if not jewelry:
        return jsonify({"error": "jewelry does not exist"}), 404
    else:
        return jsonify({
            "id": jewelry.id,
            "title": jewelry.title,
            "country": jewelry.country,
            "created": jewelry.created,
            "object_place": jewelry.object_place,
            "medium": jewelry.medium
        }), 201


@museums.delete("/<int:m_id>/jewelries/<int:p_id>")
def delete_museum_jewelry(m_id, p_id):
    museum = Museum.query.filter_by(id=m_id).first()

    if not museum:
        return jsonify({"error": "museum does not exist"}), 404
    sculpture = Sculpture.query.filter_by(place=museum, id=p_id).first()
    if not jewelry:
        return jsonify({"error": "jewelry does not exist"}), 404

    db.session.delete(sculpture)
    db.session.commit()

    return jsonify({"message": "jewelry deleted"}), 204
