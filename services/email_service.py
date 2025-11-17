from flask import current_app
from app import mail
from flask_mail import Message
import os

from domain.models.certificate import Certificate
from domain.models.user import User
from exceptions.business_exceptions import BadRequestException


def send_password_reset_email(user_email: str, token: str):
    msg = Message(
        subject="Redefinição de senha - Event Anexus",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[user_email],
        body=f"""Olá,

            Você solicitou a redefinição de senha da sua conta no Event Anexus.

            Seu código de verificação é: {token}

            Este código é válido por 5 minutos.

            Se você não solicitou esta redefinição, ignore este email e sua senha permanecerá inalterada.

            Atenciosamente,
            Equipe Event Anexus
    """
    )

    try:
        mail.send(msg)
    except Exception as e:
        raise Exception("Erro ao enviar email de redefinição de senha.") from e


def send_certificate_by_email(certificate: Certificate, destination_user: User):
    """Envia certificado por email"""
    try:
        msg = Message(
            subject=f"Certificado de Participação - {certificate.event.title}",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[destination_user.email],
            body=f"""
            Olá {destination_user.name},
            
            Segue em anexo seu certificado de participação do evento "{certificate.event.title}".
            
            Parabéns pela participação!
            
            Atenciosamente,
            Sistema Event Anexus
            """
        )

        # Anexar PDF
        with open(certificate.certificate_path, 'rb') as f:
            msg.attach(
                filename=f"certificado_{certificate.event.title}.pdf",
                content_type="application/pdf",
                data=f.read()
            )

        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Erro ao enviar certificado por email: {str(e)}")
        raise BadRequestException(
            details=[{"email": "Erro ao enviar certificado por email"}])
