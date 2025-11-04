from exceptions import UnauthorizedException, BadRequestException
from models import User
from services import email_service, user_service


def login(email: str, password: str) -> str:
    if not email or not password:
        raise BadRequestException("Email e senha são obrigatórios.")

    user: User = user_service.find_user_by_email(email)
    if not user or not user.check_password(password):
        raise UnauthorizedException("Credenciais inválidas.")

    return user.generate_auth_token()


def reset_password(email: str):
    if not email:
        raise BadRequestException("Email é obrigatório.")

    token = user_service.generate_user_reset_token(email)
    email_service.send_password_reset_email(email, token)


def verify_reset_token(token: str, new_password: str):
    if not token or not new_password:
        raise BadRequestException("Token e nova senha são obrigatórios.")

    user_service.change_user_password(token, new_password)
