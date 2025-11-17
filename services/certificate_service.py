import os
from datetime import datetime, timedelta
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, darkblue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from flask import current_app
from flask_mail import Message

from app import db
from domain.models import Certificate, Event, User, event_participants
from services import email_service
from exceptions import BadRequestException, NotFoundException


class CertificateService:

    @staticmethod
    def _get_certificates_dir():
        """Cria e retorna o diretório para armazenar certificados"""
        certificates_dir = Path(current_app.instance_path) / "certificates"
        certificates_dir.mkdir(parents=True, exist_ok=True)
        return certificates_dir

    @staticmethod
    def _generate_certificate_pdf(user: User, event: Event) -> str:
        """Gera o PDF do certificado e retorna o caminho do arquivo"""
        # Debug: verificar se o usuário tem nome
        current_app.logger.info(
            f"Gerando certificado para: {user.name} (ID: {user.id})")

        certificates_dir = CertificateService._get_certificates_dir()
        filename = f"certificate_{user.id}_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = certificates_dir / filename

        # Configurar documento PDF
        doc = SimpleDocTemplate(str(filepath), pagesize=A4,
                                rightMargin=2 * cm, leftMargin=2 * cm,
                                topMargin=3 * cm, bottomMargin=3 * cm)

        # Estilos
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=black,
            fontName='Helvetica-Bold'
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=15,
            alignment=TA_JUSTIFY,
            textColor=black,
            fontName='Helvetica'
        )

        center_style = ParagraphStyle(
            'CustomCenter',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=black,
            fontName='Helvetica'
        )

        # Conteúdo do certificado
        story = []

        # Título
        story.append(Paragraph("CERTIFICADO DE PARTICIPAÇÃO", title_style))
        story.append(Spacer(1, 20))

        # Texto principal
        story.append(Paragraph("Certificamos que", body_style))
        story.append(Spacer(1, 10))

        # Nome do participante
        participant_name = getattr(user, 'name', 'Nome não disponível')
        story.append(Paragraph(f"<b>{participant_name}</b>", subtitle_style))
        story.append(Spacer(1, 20))

        # Texto do evento
        event_date = event.date.strftime(
            "%d de %B de %Y") if event.date else "Data não informada"
        event_time = event.date.strftime("%H:%M") if event.date else ""

        participation_text = f"""
        participou do evento <b>"{event.title}"</b>, realizado em {event_date}
        {f" às {event_time}" if event_time else ""}, no local {event.location}.
        """

        if event.speaker:
            participation_text += f"""<br/><br/>
            O evento foi conduzido por <b>{event.speaker}</b>.
            """

        story.append(Paragraph(participation_text, body_style))
        story.append(Spacer(1, 30))

        # Instituição organizadora
        story.append(Paragraph(f"<b>{event.institution_organizer}</b>", center_style))
        story.append(Spacer(1, 10))

        # Data de emissão
        emission_date = datetime.now().strftime("%d de %B de %Y")
        story.append(Paragraph(f"Emitido em {emission_date}", center_style))
        story.append(Spacer(1, 30))

        # Assinatura (texto simples por enquanto)
        story.append(Paragraph("_" * 40, center_style))
        story.append(Paragraph("Assinatura do Responsável", center_style))

        # Gerar PDF
        doc.build(story)

        return str(filepath)

    @staticmethod
    def generate_certificate_for_participant(user_id: int, event_id: int) -> Certificate:
        """Gera certificado para um participante específico"""
        user = User.query.filter_by(id=user_id, active=True).first()
        if not user:
            raise NotFoundException("Usuário não encontrado")

        event = Event.query.filter_by(id=event_id, active=True).first()
        if not event:
            raise NotFoundException("Evento não encontrado")

        # Verificar se o evento já foi concluído
        if event.date > datetime.now():
            raise BadRequestException(
                details=[
                    {"event": "Certificados só podem ser gerados após a conclusão do evento"}]
            )

        # Verificar se o usuário estava inscrito no evento
        participation = db.session.query(event_participants).filter_by(
            user_id=user_id,
            event_id=event_id,
            active=True
        ).first()

        if not participation:
            raise BadRequestException(
                details=[{"participation": "Usuário não estava inscrito neste evento"}]
            )

        # Verificar se já existe certificado
        existing_certificate = Certificate.query.filter_by(
            user_id=user_id,
            event_id=event_id,
            active=True
        ).first()

        if existing_certificate:
            return existing_certificate

        # Gerar PDF
        certificate_path = CertificateService._generate_certificate_pdf(user, event)

        # Salvar no banco
        certificate = Certificate(
            user_id=user_id,
            event_id=event_id,
            certificate_path=certificate_path
        )

        db.session.add(certificate)
        db.session.commit()

        return certificate

    @staticmethod
    def generate_certificates_for_event(event_id: int) -> list[Certificate]:
        """Gera certificados para todos os participantes de um evento"""
        event = Event.query.filter_by(id=event_id, active=True).first()
        if not event:
            raise NotFoundException("Evento não encontrado")

        # Verificar se o evento já foi concluído
        if event.date > datetime.now():
            raise BadRequestException(
                details=[
                    {"event": "Certificados só podem ser gerados após a conclusão do evento"}]
            )

        # Buscar todos os participantes inscritos
        participants = db.session.query(User).join(
            event_participants,
            User.id == event_participants.c.user_id
        ).filter(
            event_participants.c.event_id == event_id,
            event_participants.c.active == True,
            User.active == True
        ).all()

        certificates = []
        for user in participants:
            try:
                certificate = CertificateService.generate_certificate_for_participant(
                    user.id, event_id
                )
                certificates.append(certificate)
            except Exception as e:
                # Log error but continue with other participants
                current_app.logger.error(
                    f"Erro ao gerar certificado para usuário {user.id}: {str(e)}")
                continue

        return certificates

    @staticmethod
    def get_user_certificates(user_id: int) -> list[Certificate]:
        """Retorna todos os certificados de um usuário"""
        return Certificate.query.filter_by(
            user_id=user_id,
            active=True
        ).order_by(Certificate.generated_at.desc()).all()

    @staticmethod
    def get_certificate_by_id(certificate_id: int, user_id: int = None) -> Certificate:
        """Retorna um certificado específico"""
        query = Certificate.query.filter_by(id=certificate_id, active=True)

        if user_id:
            query = query.filter_by(user_id=user_id)

        certificate = query.first()
        if not certificate:
            raise NotFoundException("Certificado não encontrado")

        return certificate

    @staticmethod
    def process_completed_events():
        """Processa eventos concluídos para gerar certificados automaticamente"""
        # Buscar eventos que foram concluídos recentemente (nas últimas 24h)
        yesterday = datetime.now() - timedelta(days=1)

        completed_events = Event.query.filter(
            Event.active == True,
            Event.date <= datetime.now(),
            Event.date >= yesterday
        ).all()

        for event in completed_events:
            try:
                # Verificar se já foram gerados certificados para este evento
                existing_certificates = Certificate.query.filter_by(
                    event_id=event.id,
                    active=True
                ).count()

                # Contar participantes inscritos
                participants_count = db.session.query(event_participants).filter_by(
                    event_id=event.id,
                    active=True
                ).count()

                # Se ainda não foram gerados certificados para todos
                if existing_certificates < participants_count:
                    certificates = CertificateService.generate_certificates_for_event(
                        event.id)

                    # Enviar por email
                    for certificate in certificates:
                        try:
                            email_service.send_certificate_by_email(
                                certificate, certificate.user)
                        except Exception as e:
                            current_app.logger.error(
                                f"Erro ao enviar certificado {certificate.id}: {str(e)}")
                            continue

            except Exception as e:
                current_app.logger.error(
                    f"Erro ao processar evento {event.id}: {str(e)}")
                continue
