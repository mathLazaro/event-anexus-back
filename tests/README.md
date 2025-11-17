# Testes Unitários - Event Anexus

Este diretório contém testes unitários para os requisitos funcionais **RFC05** (Login/Recuperação de senha) e **RFC01** (CRUD usuário).

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py                 # Inicialização do módulo de testes
├── conftest.py                 # Configurações e fixtures compartilhadas
├── test_auth.py                # Testes para RFC05 - Login/Recuperação de senha
└── test_user.py                # Testes para RFC01 - CRUD usuário
```

## 🚀 Como Executar os Testes

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar testes específicos

```bash
# Testes do RFC05 (Login/Recuperação de senha)
pytest tests/test_auth_rfc05.py -v

# Testes do RFC01 (CRUD usuário)
pytest tests/test_user_rfc01.py -v

# Teste específico
pytest tests/test_auth_rfc05.py::TestAuthService::test_login_success -v
```

### Executar com relatório de cobertura

```bash
pytest tests/ --cov=services --cov=routes --cov-report=html
```

## 📊 Status dos Testes

### RFC05 - Login/Recuperação de senha ✅

-   **12/12 testes passando** nos services
-   **5/6 testes passando** nas rotas
-   **Total: 17/18 testes (94.4%)**

#### Testes de Service (100% ✅)

-   ✅ Login com credenciais válidas
-   ✅ Login com email/senha inválidos
-   ✅ Login com campos vazios/nulos
-   ✅ Reset de senha com email válido
-   ✅ Reset com email vazio/nulo
-   ✅ Verificação de token de reset

#### Testes de Rotas (83.3% ✅)

-   ✅ Login via API
-   ✅ Login com credenciais inválidas
-   ✅ Login com dados faltando
-   ✅ Reset de senha via API
-   ✅ Reset com usuário inexistente
-   ❌ Verificação de token via API (erro 500)

### RFC01 - CRUD usuário 📝

-   **9/16 testes passando** nos services
-   **1/9 testes passando** nas rotas
-   **Total: 10/25 testes (40%)**

#### Testes de Service (56.25% ✅)

-   ✅ Busca de usuário por ID
-   ✅ Busca com ID inexistente
-   ✅ Busca com ID inválido
-   ✅ Busca de usuário por email
-   ✅ Busca com email inexistente
-   ✅ Busca com email vazio
-   ❌ Criação de usuário (erro na validação)
-   ❌ Atualização de usuário (método não existe)
-   ❌ Exclusão de usuário (método não existe)
-   ✅ Listagem de usuários
-   ❌ Listagem com paginação (parâmetros não suportados)

#### Testes de Rotas (11.1% ✅)

-   ❌ Criação via API (redirect 308)
-   ❌ Busca via API (token format)
-   ❌ Atualização via API (token format)
-   ❌ Exclusão via API (token format)
-   ❌ Listagem via API (token format)
-   ✅ Acesso não autorizado
-   ❌ Validação de email inválido (redirect 308)
-   ❌ Validação de senha fraca (redirect 308)

## 🐛 Problemas Identificados

### 1. User Service - Métodos Faltando

```python
# Métodos que precisam ser implementados/corrigidos:
- create_user(data: dict) -> User
- update_user(user_id: int, data: dict) -> User
- delete_user(user_id: int) -> None
- list_users(page: int, per_page: int) -> Pagination
```

### 2. API Response Format

```python
# Login retorna 'token' mas testes esperam 'access_token'
# auth_routes.py linha ~XX
response = {'token': token}  # ❌
response = {'access_token': token}  # ✅
```

### 3. Rotas com Redirect 308

```python
# URLs com trailing slash causando redirects
'/users'   # ❌ redirect
'/users/'  # ✅ correto
```

## 🧪 Fixtures e Helpers

### `conftest.py`

-   **`app`**: Fixture da aplicação Flask para testes
-   **`client`**: Cliente HTTP para testes de rotas
-   **`create_test_user()`**: Helper para criar usuários de teste
-   **`get_auth_headers()`**: Helper para obter headers de autenticação

### Configuração de Teste

```python
# Base de dados SQLite em memória
SQLALCHEMY_DATABASE_URI = 'sqlite:///temp_test.db'
TESTING = True
MAIL_SUPPRESS_SEND = True  # Não enviar emails reais
```

## 📈 Próximos Passos

1. **Corrigir User Service**: Implementar métodos CRUD faltando
2. **Ajustar Response Format**: Padronizar 'access_token' nas rotas
3. **Corrigir URLs**: Adicionar trailing slashes nas rotas
4. **Implementar Validações**: Email format, password strength
5. **Adicionar Coverage**: Instalar pytest-cov para relatórios
6. **Testes de Performance**: Adicionar testes de carga se necessário

## 🎯 Meta de Cobertura

-   **RFC05**: ✅ **94.4%** (Quase completo!)
-   **RFC01**: 📝 **40%** (Precisa implementação)
-   **Geral**: **62.8%** (Boa base, melhorar RFC01)

---

## 💡 Comandos Úteis

```bash
# Instalar dependências de teste
pip install pytest pytest-flask pytest-mock pytest-cov

# Executar com menos verbosidade
pytest tests/ --tb=short

# Executar apenas testes que falharam
pytest tests/ --lf

# Executar em paralelo (mais rápido)
pip install pytest-xdist
pytest tests/ -n auto
```
