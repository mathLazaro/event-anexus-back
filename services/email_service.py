from app import mail
from flask_mail import Message
import os


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
