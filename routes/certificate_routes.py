from flask import Blueprint, request, current_app, send_file
from flask_jwt_extended import jwt_required, current_user
from flasgger import swag_from
import os

import services.certificate_service as service
import services.email_service as email_service
import docs.certificates_docs as swagger
from exceptions import *
from utils.response import *


certificate_bp = Blueprint("certificate_bp", __name__, url_prefix="/certificates")


@certificate_bp.route("/", methods=["GET"])
@swag_from(swagger.list_my_certificates)
@jwt_required()
def list_my_certificates():
    """Lista todos os certificados do usuário autenticado"""
    try:
        certificates = service.CertificateService.get_user_certificates(current_user.id)
        return response_resource([cert.to_dict() for cert in certificates])
    except Exception as e:
        print(e)
        raise


@certificate_bp.route("/<int:certificate_id>", methods=["GET"])
@swag_from(swagger.get_certificate)
@jwt_required()
def get_certificate(certificate_id):
    """Obter detalhes de um certificado específico"""
    try:
        certificate = service.CertificateService.get_certificate_by_id(
            certificate_id, current_user.id)
        return response_resource(certificate.to_dict())
    except Exception as e:
        print(e)
        raise


@certificate_bp.route("/<int:certificate_id>/download", methods=["GET"])
@swag_from(swagger.download_certificate)
@jwt_required()
def download_certificate(certificate_id):
    """Baixar o PDF do certificado"""
    try:
        certificate = service.CertificateService.get_certificate_by_id(
            certificate_id, current_user.id)

        if not os.path.exists(certificate.certificate_path):
            raise NotFoundException("Arquivo do certificado não encontrado")

        # Nome do arquivo para download
        filename = f"certificado_{certificate.event.title.replace(' ', '_')}_{certificate.user.name.replace(' ', '_')}.pdf"

        return send_file(
            certificate.certificate_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(e)
        raise


@certificate_bp.route("/<int:certificate_id>/send-email", methods=["POST"])
@swag_from(swagger.send_certificate_email)
@jwt_required()
def send_certificate_email(certificate_id):
    """Reenviar certificado por email"""
    try:
        certificate = service.CertificateService.get_certificate_by_id(
            certificate_id, current_user.id)
        email_service.send_certificate_by_email(certificate, current_user)
        return response_resource({"message": "Certificado enviado por email com sucesso"})
    except Exception as e:
        print(e)
        raise


@certificate_bp.route("/event/<int:event_id>/generate", methods=["POST"])
@swag_from(swagger.generate_certificate_for_event)
@jwt_required()
def generate_certificate_for_event(event_id):
    """Gerar certificado para o usuário autenticado em um evento específico"""
    try:
        certificate = service.CertificateService.generate_certificate_for_participant(
            current_user.id, event_id
        )
        return response_created("certificate", certificate.id, "Certificado gerado com sucesso")
    except Exception as e:
        print(e)
        raise
