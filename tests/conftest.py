import pytest
import os

os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
os.environ['TESTING'] = '1'


@pytest.fixture(scope='function')
def app():
    """
    Cria uma instância da aplicação para testes com banco de dados EM MEMÓRIA.

    IMPORTANTE: Este fixture usa SQLite EM MEMÓRIA (sqlite:///:memory:) que é:
    - Criado TOTALMENTE na RAM, sem tocar o disco
    - Completamente separado do banco de produção (instance/database.db)
    - Automaticamente destruído quando o teste termina
    - ZERO possibilidade de afetar o banco de produção

    O banco de produção NUNCA é tocado pelos testes!
    """
    from app import create_app, db

    test_app = create_app()

    # Garantir que as configurações de teste estão ativas
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['MAIL_SUPPRESS_SEND'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False
    test_app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    test_app.config['SQLALCHEMY_ECHO'] = False

    with test_app.app_context():
        # Criar todas as tabelas no banco EM MEMÓRIA
        db.create_all()

        yield test_app

        # Limpar sessão
        db.session.remove()
        # Dropar tabelas (apenas do banco em memória - que já vai sumir)
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de teste para fazer requisições"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner para comandos CLI"""
    return app.test_cli_runner()


def create_test_user(name="João Silva", email="joao@test.com", password="123456", user_type=None):
    """Helper para criar usuário de teste"""
    from app import db
    from domain.models import User, UserType

    if user_type is None:
        user_type = UserType.REGULAR

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
