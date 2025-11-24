from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from services import report_service
import docs.reports_docs as report_docs

report_bp = Blueprint('report', __name__, url_prefix='/reports')


@report_bp.route('/events-by-type', methods=['GET'])
@jwt_required()
@swag_from(report_docs.get_events_by_type)
def get_events_by_type():
    """
    Retorna relatório de quantidade de eventos por tipo.
    Formato ideal para gráfico de pizza.
    """
    try:
        data = report_service.get_events_by_type_report()
        return jsonify(data), 200
    except Exception as e:
        print(f"Erro ao gerar relatório de eventos por tipo: {e}")
        return jsonify({"message": "Erro ao gerar relatório"}), 500


@report_bp.route('/events-summary', methods=['GET'])
@jwt_required()
@swag_from(report_docs.get_events_summary)
def get_events_summary():
    """
    Retorna estatísticas resumidas de eventos.
    Inclui totais, eventos por tipo, tipo mais/menos comum.
    """
    try:
        data = report_service.get_events_summary_statistics()
        return jsonify(data), 200
    except Exception as e:
        print(f"Erro ao gerar resumo de eventos: {e}")
        return jsonify({"message": "Erro ao gerar resumo"}), 500


@report_bp.route('/top-engagement', methods=['GET'])
@jwt_required()
@swag_from(report_docs.get_top_engagement_events)
def get_top_engagement():
    """
    Retorna top 10 eventos com maior engajamento.
    Aceita parâmetro opcional 'type' para filtrar por tipo de evento.
    """
    try:
        event_type = request.args.get('type')
        data = report_service.get_top_engagement_events_report(event_type)
        return jsonify(data), 200
    except Exception as e:
        print(f"Erro ao gerar relatório de engajamento: {e}")
        return jsonify({"message": "Erro ao gerar relatório de engajamento"}), 500
