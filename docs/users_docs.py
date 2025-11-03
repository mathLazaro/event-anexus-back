list_users = {
    "tags": ["Usuários"],
    "summary": "Listar usuários",
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
                        "adm": {"type": "boolean"}
                    }
                },
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
                    'adm': {'type': 'boolean'}
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
    'parameters': [
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
                    'adm': {'type': 'boolean'}
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
    'parameters': [
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
    'parameters': [
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
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'telephone_number': {'type': 'string'},
                    'department': {'type': 'string'},
                    'adm': {'type': 'boolean'}
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
                    'adm': {'type': 'boolean'}
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
