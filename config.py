import os
from pathlib import Path
import docs.events_docs as swagger

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "database.db"


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{DB_PATH}")
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
        ],
        # Expor o schema do EventFilterDTO nas definitions para que o Swagger UI o mostre
        'definitions': {
            'EventFilterDTO': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                    'date_from': {'type': 'string', 'format': 'date-time', 'example': '2025-12-01T00:00:00'},
                    'date_to': {'type': 'string', 'format': 'date-time', 'example': '2025-12-31T23:59:59'},
                    'location': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['WORKSHOP', 'LECTURE', 'CONFERENCE', 'SEMINAR', 'HACKATHON', 'MEETUP', 'TRAINING', 'WEBINAR', 'OTHER']},
                    'speaker': {'type': 'string'},
                    'institution_organizer': {'type': 'string'},
                    'created_by': {'type': 'integer'},
                    'q': {'type': 'string', 'description': 'Pesquisa livre: title | description | location | speaker | institution_organizer'},
                    'order_by': {'type': 'string', 'enum': ['date', 'title', 'capacity', 'location', 'type', 'speaker', 'institution_organizer'], 'default': 'date'},
                    'order_direction': {'type': 'string', 'enum': ['asc', 'desc'], 'default': 'asc'}
                }
            }
        }
    }
