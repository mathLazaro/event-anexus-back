import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "database.db"


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-chave-secreta")
