from flasgger import swag_from
from flask import Blueprint, jsonify, request
import services.auth_service as service
import services.user_service as user_service
import docs.auth_docs as swagger

from exceptions.business_exceptions import BadRequestException

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
@swag_from(swagger.login)
def login():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")
        email = data.get("email")
        password = data.get("password")
        token = service.login(email, password)
        user = user_service.find_user_by_email(email)
        return jsonify({"message": "Login bem sucedido", "token": token, "user": user.to_dict()}), 200
    except Exception as e:
        print(e)
        raise


@auth_bp.route("/reset-password", methods=["POST"])
@swag_from(swagger.reset_password)
def reset_password():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")
        email = data.get("email")
        service.reset_password(email)
        return jsonify({"message": "Instruções para redefinição de senha enviadas para o email."}), 200
    except Exception as e:
        print(e)
        raise


@auth_bp.route("/verify-reset-password", methods=["POST"])
@swag_from(swagger.verify_reset_token)
def verify_reset_token():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequestException("Body deve ser um JSON")
        token = data.get("token")
        new_password = data.get("new_password")
        service.verify_reset_token(token, new_password)
        return jsonify({"message": "Token de redefinição de senha verificado com sucesso."}), 200
    except Exception as e:
        print(e)
        raise
