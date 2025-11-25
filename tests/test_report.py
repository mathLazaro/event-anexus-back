import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from app import db
from domain.models import User, Event, EventType, UserType
from services import report_service
from exceptions import BadRequestException


class TestReportServiceEventsByType:
    """Testes para relatório de eventos por tipo"""

    def test_get_events_by_type_report_success(self, app):
        """Deve retornar relatório de eventos por tipo do usuário logado"""
        with app.app_context():
            # Criar usuário organizador
            user = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            # Criar eventos de diferentes tipos
            events_data = [
                ("Workshop 1", EventType.WORKSHOP),
                ("Workshop 2", EventType.WORKSHOP),
                ("Workshop 3", EventType.WORKSHOP),
                ("Palestra 1", EventType.LECTURE),
                ("Palestra 2", EventType.LECTURE),
                ("Seminário 1", EventType.SEMINAR),
            ]

            for title, event_type in events_data:
                event = Event(
                    title=title,
                    description="Descrição teste",
                    date=datetime.now() + timedelta(days=30),
                    location="Local Teste",
                    capacity=50,
                    type=event_type,
                    institution_organizer="UFPE",
                    created_by=user.id,
                    active=True
                )
                db.session.add(event)
            db.session.commit()

            # Mockar current_user
            with patch('services.report_service.current_user', user):
                report = report_service.get_events_by_type_report()

            # Verificações
            assert len(report) == 3  # 3 tipos diferentes
            assert report[0]['label'] == "Workshop"
            assert report[0]['value'] == 3
            assert report[0]['percentage'] == 50.0  # 3/6 = 50%

            assert report[1]['label'] == "Palestra"
            assert report[1]['value'] == 2
            assert report[1]['percentage'] == pytest.approx(33.33, 0.01)

            assert report[2]['label'] == "Seminário"
            assert report[2]['value'] == 1
            assert report[2]['percentage'] == pytest.approx(16.67, 0.01)

            # Verificar estrutura de cada item
            for item in report:
                assert 'label' in item
                assert 'value' in item
                assert 'percentage' in item
                assert 'color' in item
                assert 'type' in item

    def test_get_events_by_type_report_empty_when_no_events(self, app):
        """Deve retornar lista vazia quando usuário não tem eventos"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            with patch('services.report_service.current_user', user):
                report = report_service.get_events_by_type_report()

            assert report == []

    def test_get_events_by_type_report_ignores_inactive_events(self, app):
        """Deve ignorar eventos inativos no relatório"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            # Criar evento ativo
            event_active = Event(
                title="Workshop Ativo",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=50,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id,
                active=True
            )
            db.session.add(event_active)

            # Criar evento inativo
            event_inactive = Event(
                title="Workshop Inativo",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=50,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=user.id,
                active=False
            )
            db.session.add(event_inactive)
            db.session.commit()

            with patch('services.report_service.current_user', user):
                report = report_service.get_events_by_type_report()

            assert len(report) == 1
            assert report[0]['value'] == 1  # Apenas o ativo

    def test_get_events_by_type_report_only_current_user_events(self, app):
        """Deve retornar apenas eventos do usuário logado"""
        with app.app_context():
            # Criar dois usuários
            user1 = User(
                name="User 1",
                email="user1@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user1.encrypt_password()
            db.session.add(user1)

            user2 = User(
                name="User 2",
                email="user2@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user2.encrypt_password()
            db.session.add(user2)
            db.session.commit()

            # Criar eventos para user1
            for i in range(3):
                event = Event(
                    title=f"Workshop User1 {i}",
                    description="Descrição",
                    date=datetime.now() + timedelta(days=30),
                    location="Local",
                    capacity=50,
                    type=EventType.WORKSHOP,
                    institution_organizer="UFPE",
                    created_by=user1.id,
                    active=True
                )
                db.session.add(event)

            # Criar eventos para user2
            for i in range(5):
                event = Event(
                    title=f"Palestra User2 {i}",
                    description="Descrição",
                    date=datetime.now() + timedelta(days=30),
                    location="Local",
                    capacity=50,
                    type=EventType.LECTURE,
                    institution_organizer="UFPE",
                    created_by=user2.id,
                    active=True
                )
                db.session.add(event)
            db.session.commit()

            # Verificar relatório do user1
            with patch('services.report_service.current_user', user1):
                report = report_service.get_events_by_type_report()

            assert len(report) == 1
            assert report[0]['label'] == "Workshop"
            assert report[0]['value'] == 3


class TestReportServiceEventsSummary:
    """Testes para resumo estatístico de eventos"""

    def test_get_events_summary_statistics_success(self, app):
        """Deve retornar resumo estatístico correto"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            # Criar 5 eventos ativos e 2 inativos
            for i in range(5):
                event = Event(
                    title=f"Workshop {i}",
                    description="Descrição",
                    date=datetime.now() + timedelta(days=30),
                    location="Local",
                    capacity=50,
                    type=EventType.WORKSHOP,
                    institution_organizer="UFPE",
                    created_by=user.id,
                    active=True
                )
                db.session.add(event)

            for i in range(2):
                event = Event(
                    title=f"Palestra {i}",
                    description="Descrição",
                    date=datetime.now() + timedelta(days=30),
                    location="Local",
                    capacity=50,
                    type=EventType.LECTURE,
                    institution_organizer="UFPE",
                    created_by=user.id,
                    active=False
                )
                db.session.add(event)
            db.session.commit()

            with patch('services.report_service.current_user', user):
                summary = report_service.get_events_summary_statistics()

            assert summary['total_events'] == 7
            assert summary['active_events'] == 5
            assert summary['inactive_events'] == 2
            assert summary['most_common_type'] == "Workshop"
            assert summary['most_common_count'] == 5
            assert 'total_by_type' in summary
            assert len(summary['total_by_type']) == 1  # Apenas ativos (Workshop)

    def test_get_events_summary_statistics_empty(self, app):
        """Deve retornar zeros quando não há eventos"""
        with app.app_context():
            user = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            user.encrypt_password()
            db.session.add(user)
            db.session.commit()

            with patch('services.report_service.current_user', user):
                summary = report_service.get_events_summary_statistics()

            assert summary['total_events'] == 0
            assert summary['active_events'] == 0
            assert summary['inactive_events'] == 0
            assert summary['most_common_type'] is None
            assert summary['most_common_count'] == 0
            assert summary['least_common_type'] is None
            assert summary['least_common_count'] == 0


class TestReportServiceTopEngagement:
    """Testes para relatório de top engajamento"""

    def test_get_top_engagement_events_report_success(self, app):
        """Deve retornar top 10 eventos por engajamento"""
        with app.app_context():
            # Criar usuários
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)

            participants = []
            for i in range(50):
                participant = User(
                    name=f"Participante {i}",
                    email=f"part{i}@test.com",
                    password="12345678",
                    type=UserType.REGULAR
                )
                participant.encrypt_password()
                db.session.add(participant)
                participants.append(participant)

            db.session.commit()

            # Criar eventos com diferentes níveis de engajamento
            event1 = Event(
                title="Workshop 90% Cheio",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=10,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event1)
            db.session.flush()
            # Adicionar 9 participantes (90%)
            for i in range(9):
                event1.participants.append(participants[i])

            event2 = Event(
                title="Palestra 50% Cheio",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=20,
                type=EventType.LECTURE,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event2)
            db.session.flush()
            # Adicionar 10 participantes (50%)
            for i in range(10):
                event2.participants.append(participants[i + 10])

            event3 = Event(
                title="Seminário 100% Cheio",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=5,
                type=EventType.SEMINAR,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event3)
            db.session.flush()
            # Adicionar 5 participantes (100%)
            for i in range(5):
                event3.participants.append(participants[i + 20])

            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                report = report_service.get_top_engagement_events_report()

            # Verificações
            assert len(report) == 3

            # Deve estar ordenado por engajamento (maior primeiro)
            assert report[0]['title'] == "Seminário 100% Cheio"
            assert report[0]['engagement_percentage'] == 100.0
            assert report[0]['enrolled'] == 5
            assert report[0]['capacity'] == 5

            assert report[1]['title'] == "Workshop 90% Cheio"
            assert report[1]['engagement_percentage'] == 90.0

            assert report[2]['title'] == "Palestra 50% Cheio"
            assert report[2]['engagement_percentage'] == 50.0

            # Verificar estrutura
            for item in report:
                assert 'event_id' in item
                assert 'title' in item
                assert 'type' in item
                assert 'enrolled' in item
                assert 'capacity' in item
                assert 'engagement_percentage' in item
                assert 'color' in item

    def test_get_top_engagement_events_report_with_type_filter(self, app):
        """Deve filtrar por tipo de evento quando especificado"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            # Criar workshop
            workshop = Event(
                title="Workshop",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=10,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(workshop)

            # Criar palestra
            lecture = Event(
                title="Palestra",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=20,
                type=EventType.LECTURE,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(lecture)
            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                # Filtrar apenas workshops
                report = report_service.get_top_engagement_events_report(
                    event_type="WORKSHOP")

            assert len(report) == 1
            assert report[0]['title'] == "Workshop"
            assert report[0]['type'] == "Workshop"

    def test_get_top_engagement_events_report_limits_to_10(self, app):
        """Deve retornar no máximo 10 eventos"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            # Criar 15 eventos
            for i in range(15):
                event = Event(
                    title=f"Evento {i}",
                    description="Descrição",
                    date=datetime.now() + timedelta(days=30),
                    location="Local",
                    capacity=100,
                    type=EventType.WORKSHOP,
                    institution_organizer="UFPE",
                    created_by=organizer.id,
                    active=True
                )
                db.session.add(event)
            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                report = report_service.get_top_engagement_events_report()

            assert len(report) == 10  # Máximo de 10

    def test_get_top_engagement_events_report_ignores_zero_capacity(self, app):
        """Deve ignorar eventos sem capacidade definida"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            # Evento com capacidade
            event_with_capacity = Event(
                title="Evento com Capacidade",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=50,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event_with_capacity)

            # Evento sem capacidade
            event_no_capacity = Event(
                title="Evento sem Capacidade",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=None,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event_no_capacity)
            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                report = report_service.get_top_engagement_events_report()

            # Deve retornar apenas o evento com capacidade
            assert len(report) == 1
            assert report[0]['title'] == "Evento com Capacidade"

    def test_get_top_engagement_events_report_invalid_type_returns_empty(self, app):
        """Deve retornar lista vazia para tipo inválido"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            event = Event(
                title="Workshop",
                description="Descrição",
                date=datetime.now() + timedelta(days=30),
                location="Local",
                capacity=50,
                type=EventType.WORKSHOP,
                institution_organizer="UFPE",
                created_by=organizer.id,
                active=True
            )
            db.session.add(event)
            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                report = report_service.get_top_engagement_events_report(
                    event_type="TIPO_INVALIDO")

            assert report == []

    def test_get_top_engagement_events_report_empty_when_no_events(self, app):
        """Deve retornar lista vazia quando não há eventos"""
        with app.app_context():
            organizer = User(
                name="Organizador Test",
                email="org@test.com",
                password="12345678",
                type=UserType.ORGANIZER
            )
            organizer.encrypt_password()
            db.session.add(organizer)
            db.session.commit()

            with patch('services.report_service.current_user', organizer):
                report = report_service.get_top_engagement_events_report()

            assert report == []
