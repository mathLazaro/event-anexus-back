from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from
import services.notification_service as notification_service
from utils.response import response_resource
import docs.notifications_docs as notification_docs

notification_bp = Blueprint('notification', __name__, url_prefix='/notifications')


@notification_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from(notification_docs.list_notifications)
def list_notifications():
    """Lista notificações do usuário autenticado"""
    try:
        unread = request.args.get('unread', 'false').lower() == 'true'
        since_date = request.args.get('since_date')
        since_date = datetime.fromisoformat(since_date) if since_date else None

        notifications = notification_service.get_user_notifications(
            unread=unread,
            since_date=since_date
        )

        return response_resource([n.to_dict() for n in notifications])
    except Exception as e:
        print(f"Erro ao listar notificações: {e}")
        raise e


@notification_bp.route('/<int:notification_id>/mark-as-read', methods=['PATCH'])
@jwt_required()
@swag_from(notification_docs.mark_notification_as_read)
def mark_notification_as_read(notification_id):
    """Marca uma notificação específica como lida"""
    try:
        notification_service.mark_notification_as_read(notification_id)
        return {}, 200
    except Exception as e:
        print(f"Erro ao marcar notificação como lida: {e}")
        raise e


@notification_bp.route('/mark-all-as-read', methods=['PATCH'])
@jwt_required()
@swag_from(notification_docs.mark_all_notifications_as_read)
def mark_all_as_read():
    """Marca todas as notificações do usuário como lidas"""
    try:
        notification_service.mark_all_notifications_as_read()
        notifications = notification_service.get_user_notifications()
        return response_resource([n.to_dict() for n in notifications]), 200
    except Exception as e:
        print(f"Erro ao marcar todas as notificações como lidas: {e}")
        raise e


@notification_bp.route('/count-unread', methods=['GET'])
@jwt_required()
@swag_from(notification_docs.count_unread_notifications)
def count_unread():
    """Retorna o número de notificações não lidas do usuário"""
    try:
        count = notification_service.count_unread_notifications()
        return jsonify({"unread_count": count}), 200
    except Exception as e:
        print(f"Erro ao contar notificações não lidas: {e}")
        raise e
