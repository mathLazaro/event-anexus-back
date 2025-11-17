from exceptions import *
from config import Config
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)


db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
jwt = JWTManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    Swagger(app)

    import domain.models
    import routes

    app.register_blueprint(routes.user_bp)
    app.register_blueprint(routes.auth_bp)
    app.register_blueprint(routes.event_bp)
    app.register_blueprint(routes.certificate_bp)

    # Registrar handlers de erro
    @app.errorhandler(BadRequestException)
    def bad_request_error(error: BadRequestException):
        return {"error": error.message, "details": error.details}, 400

    @app.errorhandler(UnauthorizedException)
    def unauthorized_error(error: UnauthorizedException):
        return {"error": error.message}, 401

    @app.errorhandler(ForbiddenException)
    def forbidden_error(error: ForbiddenException):
        return {"error": error.message}, 403

    @app.errorhandler(NotFoundException)
    def not_found_error(error: NotFoundException):
        return {"error": error.message}, 404

    @app.errorhandler(Exception)
    def generic_error(error: Exception):
        return {"error": "Internal Server Error"}, 500

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> domain.User:
        identity = jwt_data["sub"]
        user = domain.User.query.filter_by(id=int(identity), active=True).first()
        if not user:
            raise UnauthorizedException("Usuário inválido.")
        return user

    from utils.certificate_scheduler import init_certificate_scheduler
    init_certificate_scheduler(app)

    return app


def def_handlers():
    pass


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
