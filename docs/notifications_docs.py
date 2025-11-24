"""
Documentação Swagger para as rotas de notificações
"""

list_notifications = {
    "tags": ["Notificações"],
    "summary": "Listar notificações do usuário",
    "description": "Retorna todas as notificações do usuário autenticado, com opção de filtrar por status de leitura e data",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "unread",
            "in": "query",
            "required": False,
            "description": "Se 'true', retorna apenas notificações não lidas",
            "schema": {
                "type": "string",
                "enum": ["true", "false"],
                "default": "false"
            }
        },
        {
            "name": "since_date",
            "in": "query",
            "required": False,
            "description": "Data inicial para filtrar notificações (formato ISO 8601)",
            "schema": {
                "type": "string",
                "format": "date-time",
                "example": "2025-01-01T00:00:00"
            }
        }
    ],
    "responses": {
        200: {
            "description": "Lista de notificações",
            "schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "example": 1
                                },
                                "user_id": {
                                    "type": "integer",
                                    "example": 5
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Novo Evento Disponível"
                                },
                                "message": {
                                    "type": "string",
                                    "example": "Um novo evento foi criado: Workshop de Python"
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-23T10:30:00"
                                },
                                "is_read": {
                                    "type": "boolean",
                                    "example": False
                                },
                                "link": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/events/42"
                                }
                            }
                        }
                    }
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
                    "message": {"type": "string", "example": "Erro ao listar notificações"}
                }
            }
        }
    }
}

mark_notification_as_read = {
    "tags": ["Notificações"],
    "summary": "Marcar notificação como lida",
    "description": "Marca uma notificação específica do usuário como lida",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "notification_id",
            "in": "path",
            "required": True,
            "description": "ID da notificação",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses": {
        200: {
            "description": "Notificação marcada como lida com sucesso",
            "schema": {
                "type": "object",
                "properties": {}
            }
        },
        404: {
            "description": "Notificação não encontrada ou não pertence ao usuário autenticado",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Notificação não encontrada"
                    }
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
            "description": "Erro interno do servidor"
        }
    }
}

mark_all_notifications_as_read = {
    "tags": ["Notificações"],
    "summary": "Marcar todas as notificações como lidas",
    "description": "Marca todas as notificações não lidas do usuário como lidas e retorna a lista atualizada de notificações",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Notificações marcadas como lidas com sucesso. Retorna todas as notificações do usuário",
            "schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "example": 1
                                },
                                "user_id": {
                                    "type": "integer",
                                    "example": 5
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Novo Evento Disponível"
                                },
                                "message": {
                                    "type": "string",
                                    "example": "Um novo evento foi criado: Workshop de Python"
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-23T10:30:00"
                                },
                                "is_read": {
                                    "type": "boolean",
                                    "example": True
                                },
                                "link": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/events/42"
                                }
                            }
                        }
                    }
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
            "description": "Erro interno do servidor"
        }
    }
}

count_unread_notifications = {
    "tags": ["Notificações"],
    "summary": "Contar notificações não lidas",
    "description": "Retorna o número de notificações não lidas do usuário autenticado",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Contador de notificações não lidas",
            "schema": {
                "type": "object",
                "properties": {
                    "unread_count": {
                        "type": "integer",
                        "example": 3,
                        "description": "Número de notificações não lidas"
                    }
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
                    "message": {
                        "type": "string",
                        "example": "Erro ao contar notificações"
                    }
                }
            }
        }
    }
}
