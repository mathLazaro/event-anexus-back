list_my_certificates = {
    "tags": ["Certificados"],
    "summary": "Listar meus certificados",
    "description": "Retorna todos os certificados do usuário autenticado, ordenados por data de geração (mais recentes primeiro).",
    "security": [{"Bearer": []}],
    "responses": {
        200: {
            "description": "Lista de certificados",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "event_id": {"type": "integer"},
                        "generated_at": {"type": "string", "format": "date-time"},
                        "certificate_path": {"type": "string"},
                        "sent_by_email": {"type": "boolean"},
                        "event": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "date": {"type": "string", "format": "date-time"},
                                "location": {"type": "string"},
                                "speaker": {"type": "string"},
                                "institution_organizer": {"type": "string"}
                            }
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

get_certificate = {
    "tags": ["Certificados"],
    "summary": "Obter detalhes do certificado",
    "description": "Retorna os detalhes de um certificado específico do usuário autenticado.",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "certificate_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do certificado"
        }
    ],
    "responses": {
        200: {
            "description": "Detalhes do certificado",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "event_id": {"type": "integer"},
                    "generated_at": {"type": "string", "format": "date-time"},
                    "certificate_path": {"type": "string"},
                    "sent_by_email": {"type": "boolean"},
                    "event": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "date": {"type": "string", "format": "date-time"},
                            "location": {"type": "string"},
                            "speaker": {"type": "string"},
                            "institution_organizer": {"type": "string"}
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
        404: {
            "description": "Certificado não encontrado",
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

download_certificate = {
    "tags": ["Certificados"],
    "summary": "Baixar certificado PDF",
    "description": "Faz o download do arquivo PDF do certificado.",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "certificate_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do certificado"
        }
    ],
    "responses": {
        200: {
            "description": "Arquivo PDF do certificado",
            "content": {
                "application/pdf": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
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
            "description": "Certificado ou arquivo não encontrado",
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

send_certificate_email = {
    "tags": ["Certificados"],
    "summary": "Reenviar certificado por email",
    "description": "Reenvia o certificado PDF para o email do usuário.",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "certificate_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID do certificado"
        }
    ],
    "responses": {
        200: {
            "description": "Certificado enviado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        },
        400: {
            "description": "Bad request - erro ao enviar email",
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
        404: {
            "description": "Certificado não encontrado",
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

generate_certificate_for_event = {
    "tags": ["Certificados"],
    "summary": "Gerar certificado para evento",
    "description": "Gera um certificado de participação para o usuário autenticado em um evento específico. Só é possível gerar após a conclusão do evento e se o usuário estava inscrito.",
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
        201: {
            "description": "Certificado gerado com sucesso",
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
            "description": "Bad request - regras de negócio violadas",
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
                            {"event": "Certificados só podem ser gerados após a conclusão do evento"},
                            {"participation": "Usuário não estava inscrito neste evento"}
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
