from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
import services.user_service as service
from exceptions import BadRequestException
from utils.response import response_created, response_resource
import docs.users_docs as swagger


user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
@swag_from(swagger.list_users)
@jwt_required()
def list_users():
    try:
        users = service.list_users()
        return response_resource([user.to_dict() for user in users])
    except Exception as e:
        print(e)


@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from(swagger.get_user)
@jwt_required()
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
            raise BadRequestException("Body deve ser um JSON")
        id = service.create_user(User.from_dict(data))

        return response_created("user", id, "Usuario criado com sucesso")
    except Exception as e:
        print(e)
        raise


@user_bp.route("/", methods=["PUT"])
@swag_from(swagger.update_user)
@jwt_required()
def update_user():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")
        user = service.update_user(User.from_dict(data))
        return jsonify(user.to_dict()), 200
    except Exception as e:
        print(e)
        raise


@user_bp.route("/", methods=["PATCH"])
@swag_from(swagger.patch_password)
@jwt_required()
def patch_password():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")
        service.patch_password(data.get("password"))
        return "", 204
    except Exception as e:
        print(e)
        raise


@user_bp.route("/", methods=["DELETE"])
@swag_from(swagger.delete_user)
@jwt_required()
def delete_user():
    try:
        service.delete_user()
        return "", 204
    except Exception as e:
        print(e)
        raise
