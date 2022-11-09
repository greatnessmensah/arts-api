from flask import Flask, jsonify
from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_first_request
    def create_tables():
        db.create_all()
    

    JWTManager(app)

    from api.routes.user import users
    from api.routes.painting import paintings
    from api.routes.sculpture import sculptures
    from api.routes.jewelry import jewelries
    from api.routes.museum import museums
    app.register_blueprint(users)
    app.register_blueprint(paintings)
    app.register_blueprint(sculptures)
    app.register_blueprint(jewelries)
    app.register_blueprint(museums)

    @app.route("/")
    def index():
        return jsonify({"message": "hello, welcome to the arts api"})

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "the server encountered an unexpected"
                        " condition that prevented it from fulfilling the request"}), 500

    return app