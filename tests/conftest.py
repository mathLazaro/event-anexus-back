import pytest
import os
import tempfile
from app import create_app, db
from domain.models import User, UserType


@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()

    # Configurar para testes
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret',
        'MAIL_SUPPRESS_SEND': True,
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Cliente de teste para fazer requisições"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner para comandos CLI"""
    return app.test_cli_runner()


def create_test_user(name="João Silva", email="joao@test.com", password="123456", user_type=UserType.REGULAR):
    """Helper para criar usuário de teste"""
    user = User()
    user.name = name
    user.email = email
    user.password = password
    user.encrypt_password()
    user.type = user_type
    user.active = True
    db.session.add(user)
    db.session.commit()
    return user
