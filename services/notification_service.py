from sqlalchemy.exc import IntegrityError
from app import db, current_user
from domain.models import Notification
from utils import parse_integrity_error
from datetime import datetime
from exceptions import NotFoundException


def save_notification(notification: Notification) -> bool:
    """
    Salva uma notificação no banco de dados.
    Args:
        notification (Notification): A notificação a ser salva.
    Returns:
        bool: True se a notificação foi salva com sucesso, False caso contrário.
    """

    try:
        db.session.add(notification)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        print(parse_integrity_error(e))
        return False
    except Exception as e:
        print(f"Erro inesperado ao salvar notificação: {e}")
        return False


def get_user_notifications(unread: bool = False, since_date : datetime = None):
    """
    Retorna as notificações do usuário atual.
    Args:
        unread (bool): Se True, retorna apenas notificações não lidas.
        since_date (datetime): Se fornecido, retorna notificações desde essa data.
    Returns:
        List[Notification]: Lista de notificações do usuário.
    """
    q = Notification.query
    q = q.filter_by(user_id=current_user.id)
    if unread:
        q = q.filter_by(is_read=False)
    if since_date:
        q = q.filter(Notification.created_at >= since_date)
    q = q.order_by(Notification.created_at.desc())
    return q.all()


def mark_notification_as_read(notification_id: int) -> bool:
    """
    Marca uma notificação como lida.
    Args:
        notification_id (int): ID da notificação a ser marcada como lida.
    Returns:
        bool: True se a notificação foi marcada como lida com sucesso, False caso contrário.
    """
    notification : Notification = Notification.query.filter_by(
        id=notification_id,
        user_id=current_user.id
    ).first()

    if not notification:
        raise NotFoundException("Notificação não encontrada")
    try:
        notification.is_read = True
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        print(parse_integrity_error(e))
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao marcar notificação como lida: {e}")
        return False


def mark_all_notifications_as_read() -> int:
    """
    Marca todas as notificações do usuário atual como lidas.
    Returns:
        int: Número de notificações marcadas como lidas.
    """
    try:
        updated_count = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).update({"is_read": True})
        db.session.commit()
        return updated_count
    except IntegrityError as e:
        db.session.rollback()
        print(parse_integrity_error(e))
        return 0
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao marcar todas as notificações como lidas: {e}")
        return 0


def count_unread_notifications() -> int:
    """
    Conta o número de notificações não lidas do usuário atual.
    Returns:
        int: Número de notificações não lidas.
    """
    return Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
