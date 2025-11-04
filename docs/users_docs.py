list_users = {
    "tags": ["Usuários"],
    "summary": "Listar usuários",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "Bearer token (formato: 'Bearer <token>')"
        }
    ],
    "responses": {
        200: {
            "description": "Lista de usuários",
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
                        "type": {"type": "string", "enum": ["ORGANIZER", "REGULAR"], "description": "Tipo do usuário"}
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
        404: {
            "description": "Resource not found",
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

create_user = {
    'tags': ['Usuários'],
    'summary': 'Criar novo usuário',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'email', 'password', 'telephone_number'],
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'telephone_number': {'type': 'string'},
                    'department': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['ORGANIZER', 'REGULAR'], 'description': 'Tipo do usuário'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'message': {'type': 'string'},
                    'url': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'details': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
}

get_user = {
    'tags': ['Usuários'],
    'summary': 'Obter usuário por ID',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (formato: \'Bearer <token>\')'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'telephone_number': {'type': 'string'},
                    'department': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['ORGANIZER', 'REGULAR'], 'description': 'Tipo do usuário'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - token inválido ou ausente',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Resource not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
}

delete_user = {
    'tags': ['Usuários'],
    'summary': 'Deletar usuário por ID',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (formato: \'Bearer <token>\')'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        204: {
            'description': 'Usuário deletado com sucesso'
        },
        401: {
            'description': 'Unauthorized - token inválido ou ausente',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Resource not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
}

update_user = {
    'tags': ['Usuários'],
    'summary': 'Atualizar usuário por ID',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (formato: \'Bearer <token>\')'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'telephone_number': {'type': 'string'},
                    'department': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['ORGANIZER', 'REGULAR'], 'description': 'Tipo do usuário'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'telephone_number': {'type': 'string'},
                    'department': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['ORGANIZER', 'REGULAR'], 'description': 'Tipo do usuário'}
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'details': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - token inválido ou ausente',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Resource not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
}

patch_password = {
    'tags': ['Usuários'],
    'summary': 'Alterar senha do usuário',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (formato: \'Bearer <token>\')'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['new_password'],
                'properties': {
                    'password': {
                        'type': 'string',
                        'minLength': 8,
                        'description': 'Nova senha (mínimo 8 caracteres)'
                    }
                }
            }
        }
    ],
    'responses': {
        204: {
            'description': 'Senha alterada com sucesso'
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'details': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'password': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - token inválido ou ausente',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Resource not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
}
