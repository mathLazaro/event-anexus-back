from flask_sqlalchemy import SQLAlchemy
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    telephone_number = db.Column(db.String(30), nullable=True)
    department = db.Column(db.String(200), nullable=True)
    adm = db.Column(db.Boolean(), default=False, nullable=False)
