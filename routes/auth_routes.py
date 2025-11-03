from flasgger import swag_from
from flask import Blueprint, jsonify, request
import services.auth_service as service
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
        return jsonify({"message": "Login bem sucedido", "token": token}), 200
    except Exception as e:
        print(e)
        raise
