from exceptions import BadRequestException, NotFoundException
from models import User
from app import db
import re
from sqlalchemy.exc import IntegrityError
from utils import parse_integrity_error


def find_user_by_id(id: int) -> User:
    if not id:
        raise BadRequestException("O id do usuário é obrigatório.")
    user = User.query.get(id)
    if not user:
        raise NotFoundException()
    return user


def list_users() -> list[User]:
    return User.query.all()


def create_user(user: User) -> int:
    validate_user_types(user)
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


def update_user(id: int, user: User) -> User:
    db_user = find_user_by_id(id)
    validate_user_types(user)
    validate_user(user)

    user.id = db_user.id
    user.password = db_user.password

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


def delete_user(id: int) -> None:
    user = find_user_by_id(id)
    db.session.delete(user)
    db.session.commit()


def validate_user_types(user: User):
    errors = []

    if not isinstance(user.name, str):
        errors.append({"name": "O nome do usuário deve ser uma string."})

    if not isinstance(user.email, str):
        errors.append({"email": "O email do usuário deve ser uma string."})

    if user.password is not None and not isinstance(user.password, str):
        errors.append({"password": "A senha do usuário deve ser uma string."})

    if user.telephone_number is not None and not isinstance(user.telephone_number, str):
        errors.append(
            {"telephone_number": "O telefone do usuário deve ser uma string."})

    if user.department is not None and not isinstance(user.department, str):
        errors.append({"department": "O departamento do usuário deve ser uma string."})

    if user.adm is not None and not isinstance(user.adm, bool):
        errors.append({"adm": "O campo adm do usuário deve ser um booleano."})

    if errors:
        raise BadRequestException("Erro de validação de tipo", errors)


def validate_user(user: User, is_sign_in: bool = False) -> None:
    errors = []
    EMAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"

    if user.name is None or user.name.strip() == "":
        errors.append({"name": "O nome do usuário é obrigatório."})

    if user.email is None or user.email.strip() == "":
        errors.append({"email": "O email do usuário é obrigatório."})
    elif not re.match(EMAIL_PATTERN, user.email):
        errors.append({"email": "O email do usuário é inválido."})

    if is_sign_in:
        if user.password is None or user.password.strip() == "":
            errors.append({"password": "A senha do usuário é obrigatória."})
        elif len(user.password) < 8:
            errors.append(
                {"password": "A senha do usuário deve ter pelo menos 8 caracteres."})

    if errors:
        raise BadRequestException("Erro de validação", errors)
