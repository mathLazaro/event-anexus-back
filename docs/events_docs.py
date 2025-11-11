list_events = {
    "tags": ["Eventos"],
    "summary": "Listar eventos do usuário autenticado",
    "description": "Retorna todos os eventos criados pelo usuário organizador autenticado",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Lista de eventos",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "date": {"type": "string", "format": "date-time", "example": "2025-12-25T00:00:00"},
                        "time": {"type": "string", "example": "14:30"},
                        "location": {"type": "string"},
                        "capacity": {"type": "integer"},
                        "type": {
                            "type": "string",
                            "enum": ["Workshop", "Lecture", "Conference", "Seminar", "Hackathon", "Meetup", "Training", "Webinar", "Other"],
                            "description": "Tipo do evento"
                        },
                        "speaker": {"type": "string"},
                        "institution_organizer": {"type": "string"},
                        "created_by": {"type": "integer"}
                    }
                },
            }
        },
        401: {
            "description": "Unauthorized - token inválido ou ausente",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        403: {
            "description": "Forbidden - usuário não tem permissão de organizador",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    },
}

get_event = {
    "tags": ["Eventos"],
    "summary": "Obter evento por ID",
    "description": "Retorna os detalhes de um evento específico",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "event_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do evento"
        }
    ],
    "responses": {
        200: {
            "description": "Evento encontrado",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "date": {"type": "string", "format": "date-time", "example": "2025-12-25T00:00:00"},
                    "time": {"type": "string", "example": "14:30"},
                    "location": {"type": "string"},
                    "capacity": {"type": "integer"},
                    "type": {
                        "type": "string",
                        "enum": ["Workshop", "Lecture", "Conference", "Seminar", "Hackathon", "Meetup", "Training", "Webinar", "Other"],
                        "description": "Tipo do evento"
                    },
                    "speaker": {"type": "string"},
                    "institution_organizer": {"type": "string"},
                    "created_by": {"type": "integer"}
                }
            }
        },
        401: {
            "description": "Unauthorized - token inválido ou ausente",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        403: {
            "description": "Forbidden - usuário não tem permissão de organizador",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Evento não encontrado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    },
}

create_event = {
    "tags": ["Eventos"],
    "summary": "Criar novo evento",
    "description": "Cria um novo evento. O campo created_by é preenchido automaticamente com o ID do usuário autenticado",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["title", "date", "time", "location", "type", "institution_organizer"],
                "properties": {
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "example": "Workshop de Python"
                    },
                    "description": {
                        "type": "string",
                        "example": "Aprenda os fundamentos de Python"
                    },
                    "date": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2025-12-25T00:00:00",
                        "description": "Data do evento (não pode ser no passado)"
                    },
                    "time": {
                        "type": "string",
                        "example": "14:30",
                        "description": "Hora do evento no formato HH:MM"
                    },
                    "location": {
                        "type": "string",
                        "maxLength": 200,
                        "example": "Auditório Principal"
                    },
                    "capacity": {
                        "type": "integer",
                        "minimum": 1,
                        "example": 50,
                        "description": "Capacidade máxima de participantes"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Workshop", "Lecture", "Conference", "Seminar", "Hackathon", "Meetup", "Training", "Webinar", "Other"],
                        "example": "Workshop"
                    },
                    "speaker": {
                        "type": "string",
                        "maxLength": 100,
                        "example": "Dr. João Silva"
                    },
                    "institution_organizer": {
                        "type": "string",
                        "maxLength": 200,
                        "example": "Universidade Federal"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Evento criado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "message": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },
        400: {
            "description": "Bad request - dados inválidos",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "details": {
                        "type": "array",
                        "items": {
                            "type": "object"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - token inválido ou ausente",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        403: {
            "description": "Forbidden - usuário não tem permissão de organizador",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    }
}

update_event = {
    "tags": ["Eventos"],
    "summary": "Atualizar evento",
    "description": "Atualiza um evento existente. Apenas o criador do evento pode atualizá-lo",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "event_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do evento"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["title", "date", "time", "location", "type", "institution_organizer"],
                "properties": {
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "example": "Workshop de Python Avançado"
                    },
                    "description": {
                        "type": "string",
                        "example": "Aprenda técnicas avançadas de Python"
                    },
                    "date": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2025-12-25T00:00:00",
                        "description": "Data do evento (não pode ser no passado)"
                    },
                    "time": {
                        "type": "string",
                        "example": "14:30",
                        "description": "Hora do evento no formato HH:MM"
                    },
                    "location": {
                        "type": "string",
                        "maxLength": 200,
                        "example": "Auditório Principal"
                    },
                    "capacity": {
                        "type": "integer",
                        "minimum": 1,
                        "example": 50,
                        "description": "Capacidade máxima de participantes"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Workshop", "Lecture", "Conference", "Seminar", "Hackathon", "Meetup", "Training", "Webinar", "Other"],
                        "example": "Workshop"
                    },
                    "speaker": {
                        "type": "string",
                        "maxLength": 100,
                        "example": "Dr. João Silva"
                    },
                    "institution_organizer": {
                        "type": "string",
                        "maxLength": 200,
                        "example": "Universidade Federal"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Evento atualizado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "message": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },
        400: {
            "description": "Bad request - dados inválidos",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "details": {
                        "type": "array",
                        "items": {
                            "type": "object"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - token inválido ou ausente ou usuário não é o criador do evento",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        403: {
            "description": "Forbidden - usuário não tem permissão de organizador",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Evento não encontrado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    }
}

delete_event = {
    "tags": ["Eventos"],
    "summary": "Deletar evento",
    "description": "Remove um evento. Apenas o criador do evento pode deletá-lo",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "event_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do evento a ser deletado"
        }
    ],
    "responses": {
        204: {
            "description": "Evento deletado com sucesso"
        },
        401: {
            "description": "Unauthorized - token inválido ou ausente ou usuário não é o criador do evento",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        403: {
            "description": "Forbidden - usuário não tem permissão de organizador",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Evento não encontrado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    }
}
