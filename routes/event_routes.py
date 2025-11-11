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
