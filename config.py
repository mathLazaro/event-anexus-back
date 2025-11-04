import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "database.db"


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-chave-secreta")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Configuração do Swagger
    SWAGGER = {
        'title': 'Event Anexus API',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'API para gerenciamento de eventos',
        'template_folder': 'templates/flasgger',
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Digite apenas o token JWT (sem o prefixo "Bearer")'
            }
        },
        'security': [
            {
                'Bearer': []
            }
        ]
    }
