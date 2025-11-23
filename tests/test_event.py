import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import db
from domain.models import User, Event, EventType, UserType, event_participants
from domain.dtos import EventFilterDTO
from services import event_service
from exceptions import BadRequestException, NotFoundException
from exceptions.business_exceptions import UnauthorizedException


class TestEventServiceCreate:
    """Testes de criação de eventos - Regras de negócio"""

    def test_create_event_success(self, app):
        """Deve criar evento com dados válidos"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                description="Workshop avançado de Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                capacity=50,
                type=EventType.WORKSHOP,
                speaker="Dr. Silva",
                institution_organizer="UFPE",
                created_by=user.id
            )

            event_id = event_service.create(event)

            assert event_id is not None
            assert isinstance(event_id, int)

            created_event = Event.query.get(event_id)
            assert created_event.title == "Workshop Python"
            assert created_event.capacity == 50

    def test_create_event_without_title_should_fail(self, app):
        """Deve rejeitar evento sem título"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("título" in str(err).lower() for err in exc.value.details)

    def test_create_event_without_date_should_fail(self, app):
        """Deve rejeitar evento sem data"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=None,
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("data" in str(err).lower() for err in exc.value.details)

    def test_create_event_with_past_date_should_fail(self, app):
        """Deve rejeitar evento com data no passado"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("passado" in str(err).lower() for err in exc.value.details)

    def test_create_event_without_location_should_fail(self, app):
        """Deve rejeitar evento sem localização"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("local" in str(err).lower() for err in exc.value.details)

    def test_create_event_without_type_should_fail(self, app):
        """Deve rejeitar evento sem tipo"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=None,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("tipo" in str(err).lower() for err in exc.value.details)

    def test_create_event_with_negative_capacity_should_fail(self, app):
        """Deve rejeitar evento com capacidade negativa"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                capacity=-10,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("capacidade" in str(err).lower() for err in exc.value.details)

    def test_create_event_without_institution_organizer_should_fail(self, app):
        """Deve rejeitar evento sem instituição organizadora"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("instituição" in str(err).lower() for err in exc.value.details)


class TestEventServiceUpdate:
    """Testes de atualização de eventos - Regras de negócio"""

    def test_update_event_success(self, app):
        """Deve atualizar evento com dados válidos"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )
            db.session.add(event)
            db.session.commit()

            updated_event = Event(
                title="Workshop Python Avançado",
                date=datetime.now() + timedelta(days=35),
                location="Sala 202",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                capacity=100
            )

            event_id = event_service.update(event.id, updated_event, user.id)

            assert event_id == event.id

            db_event = Event.query.get(event_id)
            assert db_event.title == "Workshop Python Avançado"
            assert db_event.location == "Sala 202"
            assert db_event.capacity == 100

    def test_update_nonexistent_event_should_fail(self, app):
        """Deve rejeitar atualização de evento inexistente"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            updated_event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE"
            )

            with pytest.raises(NotFoundException):
                event_service.update(99999, updated_event, user.id)

    def test_update_event_by_non_creator_should_fail(self, app):
        """Deve rejeitar atualização de evento por usuário não criador"""
        with app.app_context():
            user1 = User(
                name="Organizador 1",
                email="org1@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user1.encrypt_password()
            db.session.add(user1)

            user2 = User(
                name="Organizador 2",
                email="org2@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user2.encrypt_password()
            db.session.add(user2)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user1.id
            )
            db.session.add(event)
            db.session.commit()

            updated_event = Event(
                title="Workshop Python Avançado",
                date=datetime.now() + timedelta(days=35),
                location="Sala 202",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE"
            )

            with pytest.raises(UnauthorizedException) as exc:
                event_service.update(event.id, updated_event, user2.id)

            assert "permissão" in str(exc.value).lower()


class TestEventServiceDelete:
    """Testes de exclusão de eventos - Regras de negócio"""

    def test_delete_event_success(self, app):
        """Deve excluir evento (soft delete)"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.delete(event.id, user.id)

            db_event = Event.query.get(event.id)
            assert db_event.active == False

    def test_delete_nonexistent_event_should_fail(self, app):
        """Deve rejeitar exclusão de evento inexistente"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            with pytest.raises(NotFoundException):
                event_service.delete(99999, user.id)

    def test_delete_event_by_non_creator_should_fail(self, app):
        """Deve rejeitar exclusão de evento por usuário não criador"""
        with app.app_context():
            user1 = User(
                name="Organizador 1",
                email="org1@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user1.encrypt_password()
            db.session.add(user1)

            user2 = User(
                name="Organizador 2",
                email="org2@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user2.encrypt_password()
            db.session.add(user2)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user1.id
            )
            db.session.add(event)
            db.session.commit()

            with pytest.raises(UnauthorizedException) as exc:
                event_service.delete(event.id, user2.id)

            assert "permissão" in str(exc.value).lower()


class TestEventServiceEnrollment:
    """Testes de inscrição em eventos - Regras de negócio"""

    def test_enroll_user_in_event_success(self, app):
        """Deve inscrever usuário em evento com sucesso"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                capacity=50,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.enroll_user(event.id, participant)

            enrollment = db.session.query(event_participants).filter_by(
                event_id=event.id,
                user_id=participant.id,
                active=True
            ).first()

            assert enrollment is not None

    def test_enroll_in_past_event_should_fail(self, app):
        """Deve rejeitar inscrição em evento passado"""
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

            with pytest.raises(BadRequestException) as exc:
                event_service.enroll_user(event.id, participant)

            assert any("passado" in str(err).lower() for err in exc.value.details)

    def test_enroll_twice_in_same_event_should_fail(self, app):
        """Deve rejeitar inscrição duplicada no mesmo evento"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.enroll_user(event.id, participant)

            with pytest.raises(BadRequestException) as exc:
                event_service.enroll_user(event.id, participant)

            assert any("inscrito" in str(err).lower() for err in exc.value.details)

    def test_enroll_in_full_event_should_fail(self, app):
        """Deve rejeitar inscrição em evento lotado"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                capacity=1,  # Capacidade de apenas 1 pessoa
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.enroll_user(event.id, participant1)

            with pytest.raises(BadRequestException) as exc:
                event_service.enroll_user(event.id, participant2)

            assert any("lotado" in str(err).lower() for err in exc.value.details)

    def test_cancel_enrollment_success(self, app):
        """Deve cancelar inscrição com sucesso"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.enroll_user(event.id, participant)
            event_service.cancel_enrollment(event.id, participant)

            enrollment = db.session.query(event_participants).filter_by(
                event_id=event.id,
                user_id=participant.id,
                active=True
            ).first()

            assert enrollment is None

    def test_cancel_enrollment_in_past_event_should_fail(self, app):
        """Deve rejeitar cancelamento de inscrição em evento passado"""
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

            with pytest.raises(BadRequestException) as exc:
                event_service.cancel_enrollment(event.id, participant)

            assert any("passado" in str(err).lower() for err in exc.value.details)

    def test_cancel_nonexistent_enrollment_should_fail(self, app):
        """Deve rejeitar cancelamento de inscrição inexistente"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            with pytest.raises(NotFoundException) as exc:
                event_service.cancel_enrollment(event.id, participant)

            assert "inscrito" in str(exc.value).lower()


class TestEventServiceList:
    """Testes de listagem de eventos - Regras de negócio"""

    def test_list_events_by_organizer(self, app):
        """Deve listar apenas eventos do organizador"""
        with app.app_context():
            organizer1 = User(
                name="Organizador 1",
                email="org1@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer1.encrypt_password()
            db.session.add(organizer1)

            organizer2 = User(
                name="Organizador 2",
                email="org2@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer2.encrypt_password()
            db.session.add(organizer2)
            db.session.commit()

            event1 = Event(
                title="Workshop 1",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer1.id
            )
            db.session.add(event1)

            event2 = Event(
                title="Workshop 2",
                date=datetime.now() + timedelta(days=35),
                location="Sala 102",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer2.id
            )
            db.session.add(event2)
            db.session.commit()

            events = event_service.list_events(organizer1, None)

            assert len(events) == 1
            assert events[0].title == "Workshop 1"

    def test_list_available_events_only_future(self, app):
        """Deve listar apenas eventos futuros"""
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

            past_event = Event(
                title="Workshop Passado",
                date=datetime.now() - timedelta(days=1),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(past_event)

            future_event = Event(
                title="Workshop Futuro",
                date=datetime.now() + timedelta(days=30),
                location="Sala 102",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(future_event)
            db.session.commit()

            # Mock current_user para list_available_events
            mock_user = MagicMock()
            mock_user.id = organizer.id

            with patch('services.event_service.current_user', mock_user):
                events = event_service.list_available_events(None)

            assert len(events) == 1
            assert events[0]['title'] == "Workshop Futuro"

    def test_list_event_participants_by_organizer(self, app):
        """Deve listar participantes do evento apenas para organizador"""
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
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event)
            db.session.commit()

            event_service.enroll_user(event.id, participant)

            participants = event_service.list_event_participants(event.id, organizer.id)

            assert len(participants) == 1
            assert participants[0].id == participant.id

    def test_list_event_participants_by_non_organizer_should_fail(self, app):
        """Deve rejeitar listagem de participantes por não-organizador"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            other_user = User(
                name="Outro Usuário",
                email="outro@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            other_user.encrypt_password()
            db.session.add(other_user)
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

            with pytest.raises(UnauthorizedException) as exc:
                event_service.list_event_participants(event.id, other_user.id)

            assert "permissão" in str(exc.value).lower()

    def test_list_user_enrollments(self, app):
        """Deve listar inscrições do usuário"""
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

            event1 = Event(
                title="Workshop 1",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event1)

            event2 = Event(
                title="Workshop 2",
                date=datetime.now() + timedelta(days=35),
                location="Sala 102",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id
            )
            db.session.add(event2)
            db.session.commit()

            event_service.enroll_user(event1.id, participant)
            event_service.enroll_user(event2.id, participant)

            enrollments = event_service.list_user_enrollments(participant)

            assert len(enrollments) == 2


class TestEventServiceValidation:
    """Testes de validação de campos - Regras de negócio"""

    def test_title_max_length_validation(self, app):
        """Deve rejeitar título com mais de 100 caracteres"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="A" * 101,  # 101 caracteres
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("100 caracteres" in str(err).lower()
                       for err in exc.value.details)

    def test_location_max_length_validation(self, app):
        """Deve rejeitar local com mais de 200 caracteres"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="A" * 201,  # 201 caracteres
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("200 caracteres" in str(err).lower()
                       for err in exc.value.details)

    def test_speaker_max_length_validation(self, app):
        """Deve rejeitar palestrante com mais de 100 caracteres"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                speaker="A" * 101,  # 101 caracteres
                institution_organizer="UFPE",
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("100 caracteres" in str(err).lower()
                       for err in exc.value.details)

    def test_institution_organizer_max_length_validation(self, app):
        """Deve rejeitar instituição organizadora com mais de 200 caracteres"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="organizador@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            event = Event(
                title="Workshop Python",
                date=datetime.now() + timedelta(days=30),
                location="Sala 101",
                type=EventType.WORKSHOP,
                institution_organizer="A" * 201,  # 201 caracteres
                created_by=user.id
            )

            with pytest.raises(BadRequestException) as exc:
                event_service.create(event)

            assert any("200 caracteres" in str(err).lower()
                       for err in exc.value.details)
