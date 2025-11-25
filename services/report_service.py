from app import db, current_user
from domain.models.event import Event
from domain.models.event_type import EventType
from domain.models.event_participant import event_participants
from sqlalchemy import func, case
from typing import List, Dict, Optional


def get_events_by_type_report() -> List[Dict]:
    """
    Gera relatório de quantidade de eventos por tipo do usuário logado.
    Formato ideal para gráfico de pizza.

    Returns:
        List[Dict]: Lista de dicionários com 'label', 'value' e 'percentage'
        Exemplo:
        [
            {
                "label": "Workshop",
                "value": 15,
                "percentage": 30.0,
                "color": "#FF6384"
            },
            {
                "label": "Palestra",
                "value": 10,
                "percentage": 20.0,
                "color": "#36A2EB"
            }
        ]
    """
    # Mapeamento de tipos para labels em português
    type_labels = {
        EventType.WORKSHOP: "Workshop",
        EventType.LECTURE: "Palestra",
        EventType.CONFERENCE: "Conferência",
        EventType.SEMINAR: "Seminário",
        EventType.HACKATHON: "Hackathon",
        EventType.MEETUP: "Meetup",
        EventType.TRAINING: "Treinamento",
        EventType.WEBINAR: "Webinar",
        EventType.OTHER: "Outros"
    }

    # Cores sugeridas para gráfico de pizza (paleta harmoniosa)
    colors = [
        "#FF6384",  # Rosa
        "#36A2EB",  # Azul
        "#FFCE56",  # Amarelo
        "#4BC0C0",  # Turquesa
        "#9966FF",  # Roxo
        "#FF9F40",  # Laranja
        "#FF6384",  # Rosa claro
        "#C9CBCF",  # Cinza
        "#4D5360"   # Cinza escuro
    ]

    # Consulta agregada: conta eventos por tipo (apenas ativos e do usuário logado)
    results = db.session.query(
        Event.type,
        func.count(Event.id).label('count')
    ).filter(
        Event.active == True,
        Event.created_by == current_user.id
    ).group_by(
        Event.type
    ).all()

    # Calcular total para percentuais
    total = sum(count for _, count in results)

    # Se não houver eventos, retornar lista vazia
    if total == 0:
        return []

    # Formatar dados para o gráfico
    report_data = []
    for idx, (event_type, count) in enumerate(results):
        percentage = (count / total) * 100
        report_data.append({
            "label": type_labels.get(event_type, event_type.value),
            "value": count,
            "percentage": round(percentage, 2),
            "color": colors[idx % len(colors)],
            "type": event_type.value
        })

    # Ordenar por quantidade (maior para menor)
    report_data.sort(key=lambda x: x['value'], reverse=True)

    return report_data


def get_events_summary_statistics() -> Dict:
    """
    Gera estatísticas resumidas de eventos do usuário logado.

    Returns:
        Dict: Dicionário com estatísticas gerais
        Exemplo:
        {
            "total_events": 50,
            "active_events": 45,
            "inactive_events": 5,
            "total_by_type": [...],
            "most_common_type": "Workshop",
            "least_common_type": "Webinar"
        }
    """
    # Filtrar apenas eventos do usuário logado
    total_events = Event.query.filter_by(created_by=current_user.id).count()
    active_events = Event.query.filter_by(
        created_by=current_user.id, active=True).count()
    inactive_events = total_events - active_events

    events_by_type = get_events_by_type_report()

    most_common = events_by_type[0] if events_by_type else None
    least_common = events_by_type[-1] if events_by_type else None

    return {
        "total_events": total_events,
        "active_events": active_events,
        "inactive_events": inactive_events,
        "total_by_type": events_by_type,
        "most_common_type": most_common['label'] if most_common else None,
        "most_common_count": most_common['value'] if most_common else 0,
        "least_common_type": least_common['label'] if least_common else None,
        "least_common_count": least_common['value'] if least_common else 0
    }


def get_top_engagement_events_report(event_type: Optional[str] = None) -> List[Dict]:
    """
    Gera relatório dos top 10 eventos com maior engajamento do usuário logado.
    Engajamento = (participantes inscritos / capacidade) * 100
    Formato ideal para gráfico de barras horizontal.

    Args:
        event_type (Optional[str]): Tipo de evento para filtrar (ex: "WORKSHOP", "LECTURE")
                                     Se None, retorna todos os tipos

    Returns:
        List[Dict]: Lista de dicionários ordenados por engajamento
        Exemplo:
        [
            {
                "event_id": 42,
                "title": "Workshop Python Avançado",
                "type": "Workshop",
                "enrolled": 45,
                "capacity": 50,
                "engagement_percentage": 90.0,
                "color": "#4BC0C0"
            },
            ...
        ]
    """
    # Mapeamento de tipos para labels em português
    type_labels = {
        EventType.WORKSHOP: "Workshop",
        EventType.LECTURE: "Palestra",
        EventType.CONFERENCE: "Conferência",
        EventType.SEMINAR: "Seminário",
        EventType.HACKATHON: "Hackathon",
        EventType.MEETUP: "Meetup",
        EventType.TRAINING: "Treinamento",
        EventType.WEBINAR: "Webinar",
        EventType.OTHER: "Outros"
    }

    # Cores para o gráfico horizontal (gradiente de verde a azul)
    colors = [
        "#4BC0C0",  # Turquesa
        "#36A2EB",  # Azul
        "#9966FF",  # Roxo
        "#FF6384",  # Rosa
        "#FFCE56",  # Amarelo
        "#FF9F40",  # Laranja
        "#4D5360",  # Cinza escuro
        "#C9CBCF",  # Cinza claro
        "#66BB6A",  # Verde
        "#42A5F5"   # Azul claro
    ]

    # Construir query base
    query = db.session.query(
        Event.id,
        Event.title,
        Event.type,
        Event.capacity,
        func.count(event_participants.c.user_id).label('enrolled')
    ).outerjoin(
        event_participants,
        Event.id == event_participants.c.event_id
    ).filter(
        Event.active == True,
        Event.created_by == current_user.id,
        Event.capacity.isnot(None),
        Event.capacity > 0  # Evitar divisão por zero
    )

    # Aplicar filtro de tipo se fornecido
    if event_type:
        try:
            event_type_enum = EventType[event_type.upper()]
            query = query.filter(Event.type == event_type_enum)
        except KeyError:
            # Tipo inválido, retornar lista vazia
            return []

    # Agrupar e buscar resultados
    results = query.group_by(
        Event.id,
        Event.title,
        Event.type,
        Event.capacity
    ).all()

    # Calcular engajamento e formatar dados
    report_data = []
    for event_id, title, event_type_val, capacity, enrolled in results:
        engagement = (enrolled / capacity) * 100 if capacity > 0 else 0

        report_data.append({
            "event_id": event_id,
            "title": title,
            "type": type_labels.get(event_type_val, event_type_val.value),
            "type_key": event_type_val.value,
            "enrolled": enrolled,
            "capacity": capacity,
            "engagement_percentage": round(engagement, 2),
            "color": colors[len(report_data) % len(colors)]
        })

    # Ordenar por engajamento (maior para menor) e pegar top 10
    report_data.sort(key=lambda x: x['engagement_percentage'], reverse=True)

    return report_data[:10]
