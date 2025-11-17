import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import db
from domain.models import User, UserType
from services import auth_service
from exceptions import BadRequestException, UnauthorizedException, NotFoundException
from tests.conftest import create_test_user


class TestAuthService:
    """Testes unitários para RFC05 - Login / Recuperação de senha"""

    def test_login_success(self, app):
        """Teste de login com credenciais válidas"""
        with app.app_context():
            # Arrange
            user = create_test_user()

            # Act
            token = auth_service.login("joao@test.com", "123456")

            # Assert
            assert token is not None
            assert isinstance(token, str)

    def test_login_invalid_email(self, app):
        """Teste de login com email inválido"""
        with app.app_context():
            # Arrange
            create_test_user()

            # Act & Assert
            with pytest.raises(UnauthorizedException):
                auth_service.login("email_inexistente@test.com", "123456")

    def test_login_invalid_password(self, app):
        """Teste de login com senha inválida"""
        with app.app_context():
            # Arrange
            create_test_user()

            # Act & Assert
            with pytest.raises(UnauthorizedException):
                auth_service.login("joao@test.com", "senha_errada")

    def test_login_empty_email(self, app):
        """Teste de login com email vazio"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                auth_service.login("", "123456")

            assert "Email e senha são obrigatórios" in str(exc_info.value)

    def test_login_empty_password(self, app):
        """Teste de login com senha vazia"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                auth_service.login("joao@test.com", "")

            assert "Email e senha são obrigatórios" in str(exc_info.value)

    def test_login_none_credentials(self, app):
        """Teste de login com credenciais None"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException):
                auth_service.login(None, None)

    @patch('services.email_service.send_password_reset_email')
    @patch('services.user_service.generate_user_reset_token')
    def test_reset_password_success(self, mock_generate_token, mock_send_email, app):
        """Teste de solicitação de reset de senha com sucesso"""
        with app.app_context():
            # Arrange
            create_test_user()
            mock_generate_token.return_value = "ABC123"

            # Act
            auth_service.reset_password("joao@test.com")

            # Assert
            mock_generate_token.assert_called_once_with("joao@test.com")
            mock_send_email.assert_called_once_with("joao@test.com", "ABC123")

    def test_reset_password_empty_email(self, app):
        """Teste de reset de senha com email vazio"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                auth_service.reset_password("")

            assert "Email é obrigatório" in str(exc_info.value)

    def test_reset_password_none_email(self, app):
        """Teste de reset de senha com email None"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException):
                auth_service.reset_password(None)

    @patch('services.user_service.change_user_password')
    def test_verify_reset_token_success(self, mock_change_password, app):
        """Teste de verificação de token de reset com sucesso"""
        with app.app_context():
            # Act
            auth_service.verify_reset_token("ABC123", "nova_senha")

            # Assert
            mock_change_password.assert_called_once_with("ABC123", "nova_senha")

    def test_verify_reset_token_empty_token(self, app):
        """Teste de verificação com token vazio"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                auth_service.verify_reset_token("", "nova_senha")

            assert "Token e nova senha são obrigatórios" in str(exc_info.value)

    def test_verify_reset_token_empty_password(self, app):
        """Teste de verificação com nova senha vazia"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException) as exc_info:
                auth_service.verify_reset_token("ABC123", "")

            assert "Token e nova senha são obrigatórios" in str(exc_info.value)

    def test_login_with_inactive_user(self, app):
        """Teste de login com usuário inativo (regra de negócio)"""
        with app.app_context():
            # Arrange
            user = create_test_user()
            user.active = False
            db.session.commit()

            # Act & Assert
            with pytest.raises(UnauthorizedException):
                auth_service.login("joao@test.com", "123456")

    def test_reset_password_user_not_found(self, app):
        """Teste de reset de senha com usuário inexistente (regra de negócio)"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(NotFoundException):
                auth_service.reset_password("inexistente@test.com")

    def test_verify_reset_token_invalid_token(self, app):
        """Teste de verificação com token inexistente"""
        with app.app_context():
            # Act & Assert - token inexistente gera NotFoundException
            with pytest.raises(NotFoundException):
                auth_service.verify_reset_token("token_inexistente", "nova_senha")

    @patch('services.user_service.generate_user_reset_token')
    @patch('services.email_service.send_password_reset_email')
    def test_reset_password_integration(self, mock_send_email, mock_generate_token, app):
        """Teste de integração completa do reset de senha"""
        with app.app_context():
            # Arrange
            create_test_user()
            mock_generate_token.return_value = "ABC123"

            # Act
            auth_service.reset_password("joao@test.com")

            # Assert - verificar chamadas na ordem correta
            mock_generate_token.assert_called_once_with("joao@test.com")
            mock_send_email.assert_called_once_with("joao@test.com", "ABC123")

    def test_login_password_verification_logic(self, app):
        """Teste da lógica de verificação de senha"""
        with app.app_context():
            # Arrange
            user = create_test_user()

            # Act & Assert - senha correta
            token = auth_service.login("joao@test.com", "123456")
            assert token is not None

            # Act & Assert - senha incorreta
            with pytest.raises(UnauthorizedException):
                auth_service.login("joao@test.com", "senha_incorreta")

    def test_login_case_sensitive_email(self, app):
        """Teste de login com email case sensitive"""
        with app.app_context():
            # Arrange
            create_test_user("João", "JOAO@TEST.COM")

            # Act & Assert - deve ser case sensitive
            with pytest.raises(UnauthorizedException):
                auth_service.login("joao@test.com", "123456")  # minúsculo

            # Deve funcionar com case exato
            token = auth_service.login("JOAO@TEST.COM", "123456")
            assert token is not None

    def test_verify_reset_token_none_values(self, app):
        """Teste de verificação com valores None"""
        with app.app_context():
            # Act & Assert
            with pytest.raises(BadRequestException):
                auth_service.verify_reset_token(None, "nova_senha")

            with pytest.raises(BadRequestException):
                auth_service.verify_reset_token("ABC123", None)
