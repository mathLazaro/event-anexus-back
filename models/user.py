from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models.user_type import UserType


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    telephone_number = db.Column(db.String(30), nullable=True)
    department = db.Column(db.String(200), nullable=True)
    type = db.Column(db.Enum(UserType), nullable=False, default=UserType.REGULAR)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    @staticmethod
    def from_dict(data: dict) -> "User":
        user = User()
        for field in ['id', 'name', 'email', 'password', 'telephone_number', 'department']:
            if field in data:
                setattr(user, field, data[field])
        if 'type' in data:
            user.type = UserType(data['type'])
        return user

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "telephone_number": self.telephone_number,
            "department": self.department,
            "type": self.type.name if self.type else None,
        }

    def encrypt_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        return create_access_token(identity=str(self.id))
