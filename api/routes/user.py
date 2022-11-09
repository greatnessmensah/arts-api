from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from api.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api import db


users = Blueprint(name="users", import_name=__name__,
                 url_prefix="/users")


@users.post("/register")
def create():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(password) < 9:
        return jsonify({"error": "password is too short"}), 400

    if len(username) < 5:
        return jsonify({"error": "username is too short"}), 400

    if not username.isalnum() and " " in username:
        return jsonify({"error": "username should be alphanumeric and also no spaces"}), 400

    if not validators.email(email):
        return jsonify({"error": "email not valid"})

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email is already taken"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username is already taken"}), 409

    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created"}), 201


@users.post("/login")
def login():
    email = request.json.get("email", '')
    password = request.json.get("password", '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                "user": {
                    "refresh": refresh,
                    "access": access,
                    "username": user.username
                }
            }), 200

        return jsonify({"error": "either password or email is incorrect"}), 201


@users.get("/user")
@jwt_required()
def get():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        "username": user.username,
        "email": user.email
    }), 200



@users.get("/token/refresh")
@jwt_required()
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), 200
