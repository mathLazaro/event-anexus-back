from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from exceptions import BadRequestException, NotFoundException

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    Swagger(app)

    import models
    import routes

    app.register_blueprint(routes.user_bp)

    # Registrar handlers de erro
    @app.errorhandler(BadRequestException)
    def bad_request_error(error: BadRequestException):
        return {"error": error.message, "details": error.details}, 400

    @app.errorhandler(NotFoundException)
    def not_found_error(error: NotFoundException):
        return {"error": error.message}, 404

    @app.errorhandler(Exception)
    def generic_error(error: Exception):
        return {"error": "Internal Server Error"}, 500

    return app


def def_handlers():
    pass


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
