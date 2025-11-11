from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from flasgger import swag_from
from auth.decorators import require_organizer_grant
import services.event_service as service
import docs.events_docs as swagger
from exceptions import *
from utils.response import *
from models import Event


event_bp = Blueprint("event_bp", __name__, url_prefix="/events")


@event_bp.route("/", methods=["GET"])
@swag_from(swagger.list_events)
@jwt_required()
@require_organizer_grant()
def list_events():
    try:
        events = service.list_events(current_user)
        return response_resource([event.to_dict() for event in events])
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>", methods=["GET"])
@swag_from(swagger.get_event)
@jwt_required()
@require_organizer_grant()
def get_event(event_id):
    try:
        event = service.get_by_id(event_id)
        return response_resource(event.to_dict())
    except Exception as e:
        print(e)
        raise


@event_bp.route("/", methods=["POST"])
@swag_from(swagger.create_event)
@jwt_required()
@require_organizer_grant()
def create_event():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")

        data['created_by'] = current_user.id

        id = service.create(Event.from_dict(data))

        return response_created("event", id, "Evento criado com sucesso")
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>", methods=["PUT"])
@swag_from(swagger.update_event)
@jwt_required()
@require_organizer_grant()
def update_event(event_id):
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")

        event_id = service.update(event_id, Event.from_dict(data), current_user.id)

        return response_updated("event", event_id, "Evento atualizado com sucesso")
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>", methods=["DELETE"])
@swag_from(swagger.delete_event)
@jwt_required()
@require_organizer_grant()
def delete_event(event_id):
    try:
        service.delete(event_id, current_user.id)
        return "", 204
    except Exception as e:
        print(e)
        raise


@event_bp.route("/available", methods=["GET"])
@swag_from(swagger.list_available_events)
@jwt_required()
def list_available_events():
    """Lista eventos futuros com inscrições abertas"""
    try:
        events = service.list_available_events()
        return response_resource(events)
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>/public", methods=["GET"])
@swag_from(swagger.get_public_event)
@jwt_required()
def get_public_event(event_id):
    """Detalhes públicos do evento com vagas restantes"""
    try:
        event_details = service.get_public_event_details(event_id)
        return response_resource(event_details)
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>/enrollments", methods=["POST"])
@swag_from(swagger.enroll_in_event)
@jwt_required()
def enroll_in_event(event_id):
    """Inscrever-se em um evento"""
    try:
        service.enroll_user(event_id, current_user)
        return response_resource({"message": "Inscrição realizada com sucesso"})
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>/enrollments", methods=["DELETE"])
@swag_from(swagger.cancel_enrollment)
@jwt_required()
def cancel_enrollment(event_id):
    """Cancelar inscrição em evento"""
    try:
        service.cancel_enrollment(event_id, current_user)
        return "", 204
    except Exception as e:
        print(e)
        raise


@event_bp.route("/my-enrollments", methods=["GET"])
@swag_from(swagger.list_my_enrollments)
@jwt_required()
def list_my_enrollments():
    """Listar minhas inscrições"""
    try:
        events = service.list_user_enrollments(current_user)
        return response_resource(events)
    except Exception as e:
        print(e)
        raise


@event_bp.route("/<int:event_id>/participants", methods=["GET"])
@swag_from(swagger.list_event_participants)
@jwt_required()
@require_organizer_grant()
def list_participants(event_id):
    """Listar participantes do evento"""
    try:
        participants = service.list_event_participants(event_id, current_user.id)
        return response_resource([user.to_dict() for user in participants])
    except Exception as e:
        print(e)
        raise
