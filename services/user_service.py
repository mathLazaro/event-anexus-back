from exceptions import BadRequestException, NotFoundException
from models import User, UserType
from app import db
from flask_jwt_extended import current_user
import re
from sqlalchemy.exc import IntegrityError
from utils import parse_integrity_error


def find_user_by_id(id: int) -> User:
    if not id:
        raise BadRequestException("O id do usuário é obrigatório.")
    user = User.query.get(id)
    if not user or not user.active:
        raise NotFoundException()
    return user


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


def patch_password(new_password: str) -> None:
    if not new_password or new_password.strip() == "":
        raise BadRequestException("A nova senha do usuário é obrigatória.")
    elif len(new_password) < 8:
        raise BadRequestException(
            details=[{"password": "A nova senha do usuário deve ter pelo menos 8 caracteres."}])

    user = current_user
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
