"""
Documentação Swagger para as rotas de relatórios
"""

get_events_by_type = {
    "tags": ["Relatórios"],
    "summary": "Relatório de eventos por tipo",
    "description": "Retorna a quantidade de eventos por tipo **criados pelo usuário autenticado**, formatado para gráfico de pizza. Inclui labels em português, valores absolutos, percentuais e cores sugeridas.",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Dados do relatório de eventos por tipo",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {
                            "type": "string",
                            "example": "Workshop",
                            "description": "Nome do tipo de evento em português"
                        },
                        "value": {
                            "type": "integer",
                            "example": 15,
                            "description": "Quantidade de eventos deste tipo"
                        },
                        "percentage": {
                            "type": "number",
                            "format": "float",
                            "example": 30.0,
                            "description": "Percentual em relação ao total"
                        },
                        "color": {
                            "type": "string",
                            "example": "#FF6384",
                            "description": "Cor sugerida em hexadecimal para o gráfico"
                        },
                        "type": {
                            "type": "string",
                            "example": "WORKSHOP",
                            "description": "Tipo original do enum EventType"
                        }
                    }
                },
                "example": [
                    {
                        "label": "Workshop",
                        "value": 15,
                        "percentage": 30.0,
                        "color": "#FF6384",
                        "type": "WORKSHOP"
                    },
                    {
                        "label": "Palestra",
                        "value": 12,
                        "percentage": 24.0,
                        "color": "#36A2EB",
                        "type": "LECTURE"
                    },
                    {
                        "label": "Seminário",
                        "value": 10,
                        "percentage": 20.0,
                        "color": "#FFCE56",
                        "type": "SEMINAR"
                    }
                ]
            }
        },
        401: {
            "description": "Não autenticado",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Missing Authorization Header"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Erro ao gerar relatório"}
                }
            }
        }
    }
}

get_events_summary = {
    "tags": ["Relatórios"],
    "summary": "Resumo estatístico de eventos",
    "description": "Retorna estatísticas gerais sobre eventos **criados pelo usuário autenticado**: totais, distribuição por tipo, tipo mais/menos comum, etc.",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Estatísticas resumidas de eventos",
            "schema": {
                "type": "object",
                "properties": {
                    "total_events": {
                        "type": "integer",
                        "example": 50,
                        "description": "Total de eventos no sistema"
                    },
                    "active_events": {
                        "type": "integer",
                        "example": 45,
                        "description": "Quantidade de eventos ativos"
                    },
                    "inactive_events": {
                        "type": "integer",
                        "example": 5,
                        "description": "Quantidade de eventos inativos"
                    },
                    "total_by_type": {
                        "type": "array",
                        "description": "Distribuição completa por tipo (mesma estrutura do endpoint /events-by-type)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "value": {"type": "integer"},
                                "percentage": {"type": "number"},
                                "color": {"type": "string"},
                                "type": {"type": "string"}
                            }
                        }
                    },
                    "most_common_type": {
                        "type": "string",
                        "example": "Workshop",
                        "nullable": True,
                        "description": "Tipo de evento mais comum"
                    },
                    "most_common_count": {
                        "type": "integer",
                        "example": 15,
                        "description": "Quantidade do tipo mais comum"
                    },
                    "least_common_type": {
                        "type": "string",
                        "example": "Webinar",
                        "nullable": True,
                        "description": "Tipo de evento menos comum"
                    },
                    "least_common_count": {
                        "type": "integer",
                        "example": 5,
                        "description": "Quantidade do tipo menos comum"
                    }
                },
                "example": {
                    "total_events": 50,
                    "active_events": 45,
                    "inactive_events": 5,
                    "total_by_type": [
                        {
                            "label": "Workshop",
                            "value": 15,
                            "percentage": 30.0,
                            "color": "#FF6384",
                            "type": "WORKSHOP"
                        },
                        {
                            "label": "Palestra",
                            "value": 12,
                            "percentage": 24.0,
                            "color": "#36A2EB",
                            "type": "LECTURE"
                        }
                    ],
                    "most_common_type": "Workshop",
                    "most_common_count": 15,
                    "least_common_type": "Webinar",
                    "least_common_count": 5
                }
            }
        },
        401: {
            "description": "Não autenticado",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Missing Authorization Header"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Erro ao gerar resumo"}
                }
            }
        }
    }
}

get_top_engagement_events = {
    "tags": ["Relatórios"],
    "summary": "Top 10 eventos por engajamento",
    "description": "Retorna os 10 eventos com maior engajamento (porcentagem de inscritos em relação à capacidade) **criados pelo usuário autenticado**. Formato ideal para gráfico de barras horizontal. Aceita filtro opcional por tipo de evento.",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "type",
            "in": "query",
            "required": False,
            "description": "Tipo de evento para filtrar (opcional). Valores válidos: WORKSHOP, LECTURE, CONFERENCE, SEMINAR, HACKATHON, MEETUP, TRAINING, WEBINAR, OTHER",
            "schema": {
                "type": "string",
                "enum": ["WORKSHOP", "LECTURE", "CONFERENCE", "SEMINAR", "HACKATHON", "MEETUP", "TRAINING", "WEBINAR", "OTHER"],
                "example": "WORKSHOP"
            }
        }
    ],
    "responses": {
        200: {
            "description": "Top 10 eventos ordenados por engajamento",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "integer",
                            "example": 42,
                            "description": "ID do evento"
                        },
                        "title": {
                            "type": "string",
                            "example": "Workshop Python Avançado",
                            "description": "Título do evento"
                        },
                        "type": {
                            "type": "string",
                            "example": "Workshop",
                            "description": "Tipo do evento (label em português)"
                        },
                        "type_key": {
                            "type": "string",
                            "example": "WORKSHOP",
                            "description": "Tipo do evento (chave do enum)"
                        },
                        "enrolled": {
                            "type": "integer",
                            "example": 45,
                            "description": "Número de participantes inscritos"
                        },
                        "capacity": {
                            "type": "integer",
                            "example": 50,
                            "description": "Capacidade total do evento"
                        },
                        "engagement_percentage": {
                            "type": "number",
                            "format": "float",
                            "example": 90.0,
                            "description": "Percentual de engajamento (inscritos/capacidade)"
                        },
                        "color": {
                            "type": "string",
                            "example": "#4BC0C0",
                            "description": "Cor sugerida para o gráfico"
                        }
                    }
                },
                "example": [
                    {
                        "event_id": 42,
                        "title": "Workshop Python Avançado",
                        "type": "Workshop",
                        "type_key": "WORKSHOP",
                        "enrolled": 45,
                        "capacity": 50,
                        "engagement_percentage": 90.0,
                        "color": "#4BC0C0"
                    },
                    {
                        "event_id": 38,
                        "title": "Palestra sobre IA",
                        "type": "Palestra",
                        "type_key": "LECTURE",
                        "enrolled": 80,
                        "capacity": 100,
                        "engagement_percentage": 80.0,
                        "color": "#36A2EB"
                    },
                    {
                        "event_id": 51,
                        "title": "Hackathon 2025",
                        "type": "Hackathon",
                        "type_key": "HACKATHON",
                        "enrolled": 35,
                        "capacity": 50,
                        "engagement_percentage": 70.0,
                        "color": "#9966FF"
                    }
                ]
            }
        },
        401: {
            "description": "Não autenticado",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Missing Authorization Header"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Erro ao gerar relatório de engajamento"}
                }
            }
        }
    }
}
