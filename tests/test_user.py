import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import db
from domain.models import User, UserType
from services import user_service
from exceptions import BadRequestException, NotFoundException
from tests.conftest import create_test_user


class TestUserService:
    """Testes unitários para RFC01 - CRUD usuário"""

    def test_find_user_by_id_success(self, app):
        """Teste de busca de usuário por ID com sucesso"""
        with app.app_context():
            # Arrange
            user = create_test_user()

            # Act
            found_user = user_service.find_user_by_id(user.id)

            # Assert
            assert found_user is not None
            assert found_user.id == user.id
            assert found_user.email == "joao@test.com"

    def test_find_user_by_id_not_found(self, app):
        """Teste de busca de usuário por ID inexistente"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(NotFoundException):
                user_service.find_user_by_id(999)

    def test_find_user_by_id_invalid_id(self, app):
        """Teste de busca com ID inválido"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.find_user_by_id(None)

            assert "O id do usuário é obrigatório" in str(exc_info.value)

    def test_find_user_by_email_success(self, app):
        """Teste de busca de usuário por email com sucesso"""
        with app.app_context():
            # Arrange
            user = create_test_user()

            # Act
            found_user = user_service.find_user_by_email("joao@test.com")

            # Assert
            assert found_user is not None
            assert found_user.email == "joao@test.com"

    def test_find_user_by_email_not_found(self, app):
        """Teste de busca de usuário por email inexistente"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(NotFoundException):
                user_service.find_user_by_email("inexistente@test.com")

    def test_find_user_by_email_empty(self, app):
        """Teste de busca com email vazio"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.find_user_by_email("")

            assert "O email do usuário é obrigatório" in str(exc_info.value)

    def test_create_user_success(self, app):
        """Teste de criação de usuário com sucesso"""
        with app.app_context():
            # Arrange - create_user espera um objeto User e retorna ID
            user = User()
            user.name = "Maria Silva"
            user.email = "maria@test.com"
            user.password = "12345678"  # Mínimo 8 caracteres
            user.telephone_number = "11999999999"
            user.department = "TI"
            user.type = UserType.REGULAR

            # Act
            user_id = user_service.create_user(user)

            # Assert
            assert user_id is not None
            assert isinstance(user_id, int)

            # Verificar se foi salvo no banco
            created_user = User.query.get(user_id)
            assert created_user.name == "Maria Silva"
            assert created_user.email == "maria@test.com"
            assert created_user.telephone_number == "11999999999"
            assert created_user.department == "TI"
            assert created_user.type == UserType.REGULAR

    def test_create_user_duplicate_email(self, app):
        """Teste de criação de usuário com email duplicado"""
        with app.app_context():
            # Arrange
            create_test_user()
            user = User()
            user.name = "João Duplicado"
            user.email = "joao@test.com"  # Email já existe
            user.password = "12345678"
            user.type = UserType.REGULAR

            # Act & Assert
            with pytest.raises(BadRequestException):
                user_service.create_user(user)

    def test_create_user_missing_required_fields(self, app):
        """Teste de criação de usuário sem campos obrigatórios"""
        with app.app_context():
            # Arrange - faltam campos obrigatórios
            user = User()
            user.name = "João Incompleto"
            # Faltam email, password e type

            # Act & Assert
            with pytest.raises(BadRequestException):
                user_service.create_user(user)

    def test_create_user_invalid_email_format(self, app):
        """Teste de criação com formato de email inválido"""
        with app.app_context():
            # Arrange
            user = User()
            user.name = "João Silva"
            user.email = "email_invalido"  # Formato inválido
            user.password = "12345678"
            user.type = UserType.REGULAR

            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.create_user(user)

            # Verificar se erro é sobre email inválido nos detalhes
            details_str = str(exc_info.value.details).lower()
            assert "email" in details_str

    def test_create_user_weak_password(self, app):
        """Teste de criação com senha fraca"""
        with app.app_context():
            # Arrange
            user = User()
            user.name = "João Silva"
            user.email = "joao@test.com"
            user.password = "123"  # Senha muito curta
            user.type = UserType.REGULAR

            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.create_user(user)

            # Verificar se erro é sobre senha nos detalhes
            details_str = str(exc_info.value.details).lower()
            assert "senha" in details_str or "password" in details_str

    def test_list_users_success(self, app):
        """Teste de listagem de usuários"""
        with app.app_context():
            # Arrange
            create_test_user("João Silva", "joao@test.com")
            create_test_user("Maria Silva", "maria@test.com")
            create_test_user("Pedro Santos", "pedro@test.com")

            # Act
            users = user_service.list_users()

            # Assert
            assert len(users) == 3
            assert all(user.active for user in users)

    def test_generate_reset_token_success(self, app):
        """Teste de geração de token de reset com sucesso"""
        with app.app_context():
            # Arrange
            create_test_user()

            # Act
            token = user_service.generate_user_reset_token("joao@test.com")

            # Assert
            assert token is not None
            assert len(token) == 6  # Token de 6 caracteres

            # Verificar se foi salvo no usuário
            user = User.query.filter_by(email="joao@test.com").first()
            assert user.password_reset_token == token
            assert user.password_reset_expires_at is not None

    def test_verify_reset_token_success(self, app):
        """Teste de verificação de token válido"""
        with app.app_context():
            # Arrange
            create_test_user()
            token = user_service.generate_user_reset_token("joao@test.com")

            # Act
            user = user_service.verify_reset_token(token)

            # Assert
            assert user is not None
            assert user.email == "joao@test.com"

    def test_change_user_password_success(self, app):
        """Teste de alteração de senha com token válido"""
        with app.app_context():
            # Arrange
            create_test_user()
            token = user_service.generate_user_reset_token("joao@test.com")
            new_password = "novaSenha123"

            # Act
            user_service.change_user_password(token, new_password)

            # Assert
            user = User.query.filter_by(email="joao@test.com").first()
            assert user.check_password(new_password)  # Nova senha funciona
            assert user.password_reset_token is None  # Token foi limpo
            assert user.password_reset_expires_at is None  # Expiração foi limpa

    def test_change_user_password_invalid_token(self, app):
        """Teste de alteração com token inválido"""
        with app.app_context():
            # Arrange
            create_test_user()

            # Act & Assert - token inexistente gera NotFoundException
            with pytest.raises(NotFoundException):
                user_service.change_user_password("token_invalido", "novaSenha123")

    def test_change_user_password_empty_password(self, app):
        """Teste de alteração com senha vazia"""
        with app.app_context():
            # Arrange
            create_test_user()
            token = user_service.generate_user_reset_token("joao@test.com")

            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.change_user_password(token, "")

            details_str = str(exc_info.value).lower()
            assert "senha" in details_str or "password" in details_str

    def test_verify_reset_token_expired(self, app):
        """Teste de verificação de token expirado"""
        with app.app_context():
            # Arrange
            user = create_test_user()
            token = user_service.generate_user_reset_token("joao@test.com")

            # Simular expiração manual
            user.password_reset_expires_at = datetime.now() - timedelta(minutes=1)
            db.session.commit()

            # Act
            result = user_service.verify_reset_token(token)

            # Assert
            assert result is None  # Token expirado retorna None

            # Verificar se token foi limpo
            db.session.refresh(user)
            assert user.password_reset_token is None
            assert user.password_reset_expires_at is None

    def test_create_user_type_validation(self, app):
        """Teste de validação de tipo de usuário"""
        with app.app_context():
            # Arrange - usuário sem type
            user = User()
            user.name = "João Silva"
            user.email = "joao@test.com"
            user.password = "12345678"
            # type não definido

            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                user_service.create_user(user)

            details_str = str(exc_info.value.details).lower()
            assert "tipo" in details_str or "type" in details_str

    def test_create_user_organizer_type(self, app):
        """Teste de criação de usuário organizador"""
        with app.app_context():
            # Arrange
            user = User()
            user.name = "Maria Organizadora"
            user.email = "maria@org.com"
            user.password = "12345678"
            user.type = UserType.ORGANIZER

            # Act
            user_id = user_service.create_user(user)

            # Assert
            created_user = User.query.get(user_id)
            assert created_user.type == UserType.ORGANIZER
            assert created_user.is_organizer() == True

    def test_list_users_only_active(self, app):
        """Teste que listagem retorna apenas usuários ativos"""
        with app.app_context():
            # Arrange
            user1 = create_test_user("João", "joao@test.com")
            user2 = create_test_user("Maria", "maria@test.com")

            # Desativar um usuário
            user2.active = False
            db.session.commit()

            # Act
            users = user_service.list_users()

            # Assert
            assert len(users) == 1
            assert users[0].email == "joao@test.com"
            assert all(user.active for user in users)

    def test_find_user_by_email_case_sensitivity(self, app):
        """Teste de busca por email com case sensitivity"""
        with app.app_context():
            # Arrange
            create_test_user("João", "JOAO@TEST.COM")

            # Act & Assert - deve ser case sensitive
            with pytest.raises(NotFoundException):
                user_service.find_user_by_email("joao@test.com")  # minúsculo

            # Deve encontrar com case exato
            user = user_service.find_user_by_email("JOAO@TEST.COM")
            assert user.email == "JOAO@TEST.COM"
