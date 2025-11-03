from exceptions import UnauthorizedException, BadRequestException
from models import User


def login(email: str, password: str) -> str:
    if not email or not password:
        raise BadRequestException("Email e senha são obrigatórios.")

    user: User = User.query.filter_by(email=email, active=True).first()
    if not user or not user.check_password(password):
        raise UnauthorizedException("Credenciais inválidas.")

    return user.generate_auth_token()
