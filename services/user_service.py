from exceptions import BadRequestException, NotFoundException
from exceptions.business_exceptions import UnauthorizedException
from models import User, UserType
from app import db
from flask_jwt_extended import current_user
import re
from sqlalchemy.exc import IntegrityError
from utils import parse_integrity_error
import secrets
from datetime import datetime, timedelta
import services.event_service as event_service


def find_user_by_id(id: int) -> User:
    if not id:
        raise BadRequestException("O id do usuário é obrigatório.")
    user = User.query.get(id)
    if not user or not user.active:
        raise NotFoundException()
    return user


def find_user_by_email(email: str) -> User:
    if not email or email.strip() == "":
        raise BadRequestException("O email do usuário é obrigatório.")
    user = User.query.filter_by(email=email, active=True).first()
    if not user or not user.active:
        raise NotFoundException()
    return user


def find_user_by_reset_token(token: str) -> User:
    if not token or token.strip() == "":
        raise BadRequestException("O token de redefinição de senha é obrigatório.")
    user = User.query.filter_by(
        password_reset_token=token, active=True).first()
    if not user or not user.active:
        raise NotFoundException()
    return user


def generate_user_reset_token(email: str) -> str:
    user = find_user_by_email(email)

    token_expires_at = datetime.now() + timedelta(minutes=5)
    token = secrets.token_hex(6)[:6]

    user.password_reset_token = token
    user.password_reset_expires_at = token_expires_at

    try:
        db.session.merge(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise
    return token


def verify_reset_token(token: str) -> bool:
    user = find_user_by_reset_token(token)

    token_is_valid = str(user.password_reset_token).lower() == token.lower()
    token_is_not_expired = user.password_reset_expires_at and datetime.now(
    ) < user.password_reset_expires_at

    if not token_is_not_expired:
        user.password_reset_token = None
        user.password_reset_expires_at = None
        try:
            db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    return user if token_is_valid and token_is_not_expired else None


def change_user_password(token: str, new_password: str) -> None:
    user = verify_reset_token(token)

    if not user:
        raise BadRequestException("Token inválido ou expirado.")

    if not new_password or new_password.strip() == "":
        raise BadRequestException("A nova senha do usuário é obrigatória.")
    elif len(new_password) < 8:
        raise BadRequestException(
            details=[{"password": "A nova senha do usuário deve ter pelo menos 8 caracteres."}])

    user.password = new_password
    user.encrypt_password()

    user.password_reset_token = None
    user.password_reset_expires_at = None

    try:
        db.session.merge(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def list_users() -> list[User]:
    return User.query.filter_by(active=True).all()


def create_user(user: User) -> int:
    validate_user_types(user, is_sign_in=True)
    validate_user(user, is_sign_in=True)

    user.encrypt_password()

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise BadRequestException(details=[parse_integrity_error(e)])
    except Exception as e:
        db.session.rollback()
        raise

    return user.id


def update_user(user: User) -> User:
    db_user = current_user
    validate_user_types(user)
    validate_user(user)

    user.id = db_user.id
    user.password = db_user.password
    user.email = db_user.email
    user.type = db_user.type

    try:
        db.session.merge(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise BadRequestException(details=[parse_integrity_error(e)])
    except Exception as e:
        db.session.rollback()
        raise

    return user


def patch_password(current_password: str, new_password: str) -> None:
    if not current_password or current_password.strip() == "":
        raise BadRequestException("A senha atual do usuário é obrigatória.")
    if not new_password or new_password.strip() == "":
        raise BadRequestException("A nova senha do usuário é obrigatória.")
    elif len(new_password) < 8:
        raise BadRequestException(
            details=[{"password": "A nova senha do usuário deve ter pelo menos 8 caracteres."}])

    user: User = current_user
    if not user.check_password(current_password):
        raise UnauthorizedException("Senha atual incorreta.")

    user.password = new_password
    user.encrypt_password()

    try:
        db.session.merge(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def delete_user() -> None:
    user = current_user
    user.active = False
    db.session.merge(user)
    db.session.commit()

    event_service.deleteAllByUser(user.id)

    # TODO - Remover relacionamentos do usuário (Eventos, Convites, etc)


def validate_user_types(user: User, is_sign_in: bool = False):
    errors = []

    if not isinstance(user.name, str):
        errors.append({"name": "O nome do usuário deve ser uma string."})

    if is_sign_in:
        if not isinstance(user.email, str):
            errors.append({"email": "O email do usuário deve ser uma string."})

        if user.password is not None and not isinstance(user.password, str):
            errors.append({"password": "A senha do usuário deve ser uma string."})

    if user.telephone_number is not None and not isinstance(user.telephone_number, str):
        errors.append(
            {"telephone_number": "O telefone do usuário deve ser uma string."})

    if user.department is not None and not isinstance(user.department, str):
        errors.append({"department": "O departamento do usuário deve ser uma string."})

    if user.type is not None and not isinstance(user.type, UserType):
        errors.append({"type": "O tipo do usuário é inválido."})

    if errors:
        raise BadRequestException("Erro de validação de tipo", errors)


def validate_user(user: User, is_sign_in: bool = False) -> None:
    errors = []
    EMAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"

    if user.name is None or user.name.strip() == "":
        errors.append({"name": "O nome do usuário é obrigatório."})

    if is_sign_in:
        if user.email is None or user.email.strip() == "":
            errors.append({"email": "O email do usuário é obrigatório."})
        elif not re.match(EMAIL_PATTERN, user.email):
            errors.append({"email": "O email do usuário é inválido."})
        if user.password is None or user.password.strip() == "":
            errors.append({"password": "A senha do usuário é obrigatória."})
        elif len(user.password) < 8:
            errors.append(
                {"password": "A senha do usuário deve ter pelo menos 8 caracteres."})

    if user.type is None:
        errors.append({"type": "O tipo do usuário é obrigatório."})

    if errors:
        raise BadRequestException("Erro de validação", errors)
