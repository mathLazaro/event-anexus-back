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

# ============= DOCUMENTAÇÃO PARA INSCRIÇÕES (RFS08, RFS09, RFS10) =============

list_available_events = {
    "tags": ["Inscrições"],
    "summary": "Listar eventos disponíveis",
    "description": "Lista eventos futuros com inscrições abertas. Exibe informações resumidas e permite filtros.",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Lista de eventos disponíveis",
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

get_public_event = {
    "tags": ["Inscrições"],
    "summary": "Detalhes públicos do evento",
    "description": "Retorna detalhes completos do evento incluindo vagas restantes, quantidade de inscritos e status.",
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
            "description": "Detalhes do evento",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "date": {"type": "string", "format": "date-time"},
                    "time": {"type": "string", "example": "14:30"},
                    "location": {"type": "string"},
                    "capacity": {"type": "integer", "description": "Capacidade máxima"},
                    "type": {"type": "string"},
                    "speaker": {"type": "string"},
                    "institution_organizer": {"type": "string"},
                    "created_by": {"type": "integer"},
                    "enrolled_count": {"type": "integer", "description": "Número de participantes inscritos"},
                    "remaining_slots": {"type": "integer", "description": "Vagas restantes (null se sem limite)"},
                    "is_full": {"type": "boolean", "description": "Indica se o evento está lotado"},
                    "is_past": {"type": "boolean", "description": "Indica se o evento já passou"}
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

enroll_in_event = {
    "tags": ["Inscrições"],
    "summary": "Inscrever-se em evento",
    "description": "Realiza a inscrição do usuário autenticado no evento. Valida duplicatas, lotação e data do evento.",
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
            "description": "Inscrição realizada com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Inscrição realizada com sucesso"}
                }
            }
        },
        400: {
            "description": "Bad request - Regras de negócio violadas",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "details": {
                        "type": "array",
                        "items": {
                            "type": "object"
                        },
                        "example": [
                            {"enrollment": "Você já está inscrito neste evento."},
                            {"event": "Este evento está lotado."},
                            {"event": "Não é possível se inscrever em eventos passados."}
                        ]
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

cancel_enrollment = {
    "tags": ["Inscrições"],
    "summary": "Cancelar inscrição em evento",
    "description": "Cancela a inscrição do usuário autenticado no evento. Só permitido antes do início do evento.",
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
        204: {
            "description": "Inscrição cancelada com sucesso"
        },
        400: {
            "description": "Bad request - Não é possível cancelar",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "details": {
                        "type": "array",
                        "items": {
                            "type": "object"
                        },
                        "example": [
                            {"event": "Não é possível cancelar inscrição em eventos passados."}
                        ]
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
        404: {
            "description": "Inscrição não encontrada",
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

list_my_enrollments = {
    "tags": ["Inscrições"],
    "summary": "Listar minhas inscrições",
    "description": "Retorna todos os eventos nos quais o usuário autenticado está inscrito.",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Lista de eventos inscritos",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "date": {"type": "string", "format": "date-time"},
                        "time": {"type": "string", "example": "14:30"},
                        "location": {"type": "string"},
                        "capacity": {"type": "integer"},
                        "type": {"type": "string"},
                        "speaker": {"type": "string"},
                        "institution_organizer": {"type": "string"},
                        "created_by": {"type": "integer"}
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

list_event_participants = {
    "tags": ["Eventos"],
    "summary": "Listar participantes do evento",
    "description": "Lista todos os usuários inscritos no evento. Apenas o organizador criador do evento pode acessar.",
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
            "description": "Lista de participantes",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "telephone_number": {"type": "string"},
                        "department": {"type": "string"},
                        "type": {"type": "string", "enum": ["ORGANIZER", "REGULAR"]}
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - token inválido, ausente ou usuário não é o criador do evento",
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
