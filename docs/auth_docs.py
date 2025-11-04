login = {
    'tags': ['Autenticação'],
    'summary': 'Realizar login',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['email', 'password'],
                'properties': {
                    'email': {
                        'type': 'string',
                        'description': 'Email do usuário'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Senha do usuário'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login realizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'token': {'type': 'string', 'description': 'JWT token'},
                    'user': {
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
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - credenciais inválidas',
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

reset_password = {
    'tags': ['Autenticação'],
    'summary': 'Solicitar redefinição de senha',
    'description': 'Envia um código de verificação para o email do usuário para redefinir a senha',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['email'],
                'properties': {
                    'email': {
                        'type': 'string',
                        'description': 'Email do usuário cadastrado'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Email de redefinição enviado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Instruções para redefinição de senha enviadas para o email.'}
                }
            }
        },
        400: {
            'description': 'Bad request - email inválido ou não fornecido',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado',
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
