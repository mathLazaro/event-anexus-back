from flasgger import swag_from
from flask import Blueprint, request
from models import User
import services.user_service as service
from exceptions import BadRequestException
from utils.response import response_created, response_resource
import docs.users_docs as swagger


user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
@swag_from(swagger.list_users)
def list_users():
    try:
        users = service.list_users()
        return response_resource([user.to_dict() for user in users])
    except Exception as e:
        print(e)


@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from(swagger.get_user)
def get_user(user_id):
    try:
        if not user_id:
            raise BadRequestException("O id do usuário é obrigatório.")
        user = service.find_user_by_id(user_id)
        return response_resource(user.to_dict())
    except Exception as e:
        print(e)
        raise


@user_bp.route("/", methods=["POST"])
@swag_from(swagger.create_user)
def create_user():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body must be a valid JSON")
        id = service.create_user(User.from_dict(data))

        return response_created("user", id, "Usuario criado com sucesso")
    except Exception as e:
        print(e)
        raise


@user_bp.route("/<int:user_id>", methods=["PUT"])
@swag_from(swagger.update_user)
def update_user(user_id):
    try:
        if not user_id:
            raise BadRequestException("O id do usuário é obrigatório.")
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body must be a valid JSON")
        user = service.update_user(user_id, User.from_dict(data))
        return
    except Exception as e:
        print(e)
        raise


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from(swagger.delete_user)
def delete_user(user_id):
    try:
        if not user_id:
            raise BadRequestException("O id do usuário é obrigatório.")
        service.delete_user(user_id)
        return "", 204
    except Exception as e:
        print(e)
        raise
