from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from config import Config

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

    # Blueprints (rotas)
    # from routes.user_routes import user_bp
    # from routes.event_routes import event_bp
    # app.register_blueprint(user_bp, url_prefix="/usuarios")
    # app.register_blueprint(event_bp, url_prefix="/eventos")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
