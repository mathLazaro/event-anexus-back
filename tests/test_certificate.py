import pytest
import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from app import db
from domain.models import User, Event, EventType, UserType, Certificate, event_participants
from services.certificate_service import CertificateService
from exceptions import BadRequestException, NotFoundException


class TestCertificateServiceGeneration:
    """Testes de geração de certificados - Regras de negócio"""

    def test_generate_certificate_for_participant_success(self, app):
        """Deve gerar certificado para participante de evento concluído"""
        with app.app_context():
            # Criar organizador
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            # Criar participante
            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar evento concluído (no passado)
            event = Event(
                title="Workshop Python",
                description="Workshop concluído",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado
            certificate = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            assert certificate is not None
            assert certificate.user_id == participant.id
            assert certificate.event_id == event.id
            assert certificate.certificate_path is not None
            assert os.path.exists(certificate.certificate_path)

    def test_generate_certificate_for_future_event_should_fail(self, app):
        """Deve rejeitar geração de certificado para evento futuro"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar evento futuro
            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            with pytest.raises(BadRequestException) as exc:
                CertificateService.generate_certificate_for_participant(
                    participant.id, event.id
                )

            assert any("conclusão do evento" in str(err).lower()
                       for err in exc.value.details)

    def test_generate_certificate_for_nonexistent_user_should_fail(self, app):
        """Deve rejeitar geração de certificado para usuário inexistente"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            with pytest.raises(NotFoundException) as exc:
                CertificateService.generate_certificate_for_participant(
                    99999, event.id
                )

            assert "usuário não encontrado" in str(exc.value).lower()

    def test_generate_certificate_for_nonexistent_event_should_fail(self, app):
        """Deve rejeitar geração de certificado para evento inexistente"""
        with app.app_context():
            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            with pytest.raises(NotFoundException) as exc:
                CertificateService.generate_certificate_for_participant(
                    participant.id, 99999
                )

            assert "evento não encontrado" in str(exc.value).lower()

    def test_generate_certificate_for_non_participant_should_fail(self, app):
        """Deve rejeitar geração de certificado para usuário não inscrito"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Não inscrever o participante

            with pytest.raises(BadRequestException) as exc:
                CertificateService.generate_certificate_for_participant(
                    participant.id, event.id
                )

            assert any("não estava inscrito" in str(err).lower()
                       for err in exc.value.details)

    def test_generate_duplicate_certificate_returns_existing(self, app):
        """Deve retornar certificado existente se tentar gerar duplicado"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar primeiro certificado
            certificate1 = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            # Tentar gerar novamente
            certificate2 = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            assert certificate1.id == certificate2.id

    def test_generate_certificates_for_event_success(self, app):
        """Deve gerar certificados para todos os participantes de um evento"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant1 = User(
                name="Participante 1",
                email="p1@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant1.encrypt_password()
            db.session.add(participant1)

            participant2 = User(
                name="Participante 2",
                email="p2@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant2.encrypt_password()
            db.session.add(participant2)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participantes
            stmt = event_participants.insert().values([
                {
                    'user_id': participant1.id,
                    'event_id': event.id,
                    'registered_at': datetime.now(),
                    'active': True
                },
                {
                    'user_id': participant2.id,
                    'event_id': event.id,
                    'registered_at': datetime.now(),
                    'active': True
                }
            ])
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificados
            certificates = CertificateService.generate_certificates_for_event(event.id)

            assert len(certificates) == 2
            assert all(cert.event_id == event.id for cert in certificates)

    def test_generate_certificates_for_future_event_should_fail(self, app):
        """Deve rejeitar geração de certificados para evento futuro"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            with pytest.raises(BadRequestException) as exc:
                CertificateService.generate_certificates_for_event(event.id)

            assert any("conclusão do evento" in str(err).lower()
                       for err in exc.value.details)

    def test_generate_certificates_for_nonexistent_event_should_fail(self, app):
        """Deve rejeitar geração de certificados para evento inexistente"""
        with app.app_context():
            with pytest.raises(NotFoundException) as exc:
                CertificateService.generate_certificates_for_event(99999)

            assert "evento não encontrado" in str(exc.value).lower()


class TestCertificateServiceRetrieval:
    """Testes de recuperação de certificados - Regras de negócio"""

    def test_get_user_certificates(self, app):
        """Deve retornar todos os certificados de um usuário"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar dois eventos concluídos
            event1 = Event(
                title="Workshop 1",
                date=datetime.now() - timedelta(days=2),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event1)

            event2 = Event(
                title="Workshop 2",
                date=datetime.now() - timedelta(days=1),
                location="Sala 102",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event2)
            db.session.commit()

            # Inscrever participante nos dois eventos
            stmt = event_participants.insert().values([
                {
                    'user_id': participant.id,
                    'event_id': event1.id,
                    'registered_at': datetime.now(),
                    'active': True
                },
                {
                    'user_id': participant.id,
                    'event_id': event2.id,
                    'registered_at': datetime.now(),
                    'active': True
                }
            ])
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificados
            CertificateService.generate_certificate_for_participant(
                participant.id, event1.id
            )
            CertificateService.generate_certificate_for_participant(
                participant.id, event2.id
            )

            # Buscar certificados do usuário
            certificates = CertificateService.get_user_certificates(participant.id)

            assert len(certificates) == 2
            assert all(cert.user_id == participant.id for cert in certificates)

    def test_get_certificate_by_id_success(self, app):
        """Deve retornar certificado por ID"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado
            certificate = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            # Buscar certificado
            found_certificate = CertificateService.get_certificate_by_id(certificate.id)

            assert found_certificate.id == certificate.id
            assert found_certificate.user_id == participant.id

    def test_get_certificate_by_id_with_user_filter(self, app):
        """Deve retornar certificado filtrado por usuário"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado
            certificate = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            # Buscar certificado com filtro de usuário correto
            found_certificate = CertificateService.get_certificate_by_id(
                certificate.id, participant.id
            )

            assert found_certificate.id == certificate.id

    def test_get_certificate_by_id_wrong_user_should_fail(self, app):
        """Deve rejeitar busca de certificado com usuário incorreto"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant1 = User(
                name="Participante 1",
                email="p1@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant1.encrypt_password()
            db.session.add(participant1)

            participant2 = User(
                name="Participante 2",
                email="p2@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant2.encrypt_password()
            db.session.add(participant2)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante1
            stmt = event_participants.insert().values(
                user_id=participant1.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado para participant1
            certificate = CertificateService.generate_certificate_for_participant(
                participant1.id, event.id
            )

            # Tentar buscar com participant2
            with pytest.raises(NotFoundException) as exc:
                CertificateService.get_certificate_by_id(
                    certificate.id, participant2.id
                )

            assert "certificado não encontrado" in str(exc.value).lower()

    def test_get_nonexistent_certificate_should_fail(self, app):
        """Deve rejeitar busca de certificado inexistente"""
        with app.app_context():
            with pytest.raises(NotFoundException) as exc:
                CertificateService.get_certificate_by_id(99999)

            assert "certificado não encontrado" in str(exc.value).lower()


class TestCertificateServicePDFGeneration:
    """Testes de geração de PDF - Regras de negócio"""

    def test_pdf_file_created(self, app):
        """Deve criar arquivo PDF ao gerar certificado"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="João Silva",
                email="joao@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            event = Event(
                title="Workshop Avançado de Python",
                date=datetime.now() - timedelta(days=1),
                location="Auditório Principal",
                type=EventType.WORKSHOP,
                speaker="Dr. Maria Santos",
                institution_organizer="Universidade Federal de Pernambuco",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado
            certificate = CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            # Verificar se arquivo existe
            assert os.path.exists(certificate.certificate_path)
            assert certificate.certificate_path.endswith('.pdf')

            # Verificar tamanho do arquivo (deve ser maior que 0)
            file_size = os.path.getsize(certificate.certificate_path)
            assert file_size > 0

    def test_certificates_directory_created(self, app):
        """Deve criar diretório de certificados se não existir"""
        with app.app_context():
            certificates_dir = CertificateService._get_certificates_dir()

            assert certificates_dir.exists()
            assert certificates_dir.is_dir()


class TestCertificateServiceProcessing:
    """Testes de processamento automático - Regras de negócio"""

    def test_process_completed_events(self, app):
        """Deve processar eventos concluídos nas últimas 24h"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar evento concluído há 12 horas
            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(hours=12),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Mock email service
            with patch('services.certificate_service.email_service.send_certificate_by_email') as mock_email:
                CertificateService.process_completed_events()

            # Verificar se certificado foi gerado
            certificates = Certificate.query.filter_by(
                event_id=event.id,
                user_id=participant.id,
                active=True
            ).all()

            assert len(certificates) == 1

    def test_process_completed_events_skips_old_events(self, app):
        """Não deve processar eventos concluídos há mais de 24h"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar evento concluído há 2 dias
            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=2),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Processar eventos
            with patch('services.certificate_service.email_service.send_certificate_by_email'):
                CertificateService.process_completed_events()

            # Verificar que nenhum certificado foi gerado
            certificates = Certificate.query.filter_by(
                event_id=event.id,
                active=True
            ).all()

            assert len(certificates) == 0

    def test_process_completed_events_skips_already_processed(self, app):
        """Não deve reprocessar eventos que já tiveram certificados gerados"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participant = User(
                name="Participante Test",
                email="participante@test.com",
                password="12345678",
                type=UserType.REGULAR
            )
            participant.encrypt_password()
            db.session.add(participant)
            db.session.commit()

            # Criar evento concluído há 12 horas
            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(hours=12),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            # Inscrever participante
            stmt = event_participants.insert().values(
                user_id=participant.id,
                event_id=event.id,
                registered_at=datetime.now(),
                active=True
            )
            db.session.execute(stmt)
            db.session.commit()

            # Gerar certificado manualmente
            CertificateService.generate_certificate_for_participant(
                participant.id, event.id
            )

            # Processar eventos (não deve gerar duplicado)
            with patch('services.certificate_service.email_service.send_certificate_by_email'):
                CertificateService.process_completed_events()

            # Verificar que ainda existe apenas 1 certificado
            certificates = Certificate.query.filter_by(
                event_id=event.id,
                active=True
            ).all()

            assert len(certificates) == 1
