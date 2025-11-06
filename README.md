# 🎟️ Event Manager API

Uma API RESTful desenvolvida em **Python + Flask** para gerenciamento de eventos acadêmicos.  
O sistema permite que usuários cadastrem-se, participem de eventos e emitam certificados.

---

## 🧩 Tecnologias Utilizadas

-   **Python 3.11+**
-   **Flask**
-   **Flask-SQLAlchemy**
-   **Flask-Migrate**
-   **Flask-JWT-Extended**
-   **Flask-Swagger-UI**
-   **SQLite** (banco local)
-   **python-dotenv** (gerenciamento de variáveis de ambiente)
-   **bcrypt** (criptografia de senha)
-   **Black** (formatação de código)

---

## 📁 Estrutura de Pastas

```
project_root/
│
├── app/
│   ├── __init__.py           # Criação e configuração da aplicação
│   ├── config.py             # Configurações (banco, JWT, etc)
│   ├── models/               # Definição das entidades (SQLAlchemy)
│   ├── routes/               # Rotas e blueprints da API
│   ├── services/             # Regras de negócio e integrações
│   ├── exceptions/           # Exceptions personalizadas
│   ├── handlers/             # Global error handler
│   ├── docs/                 # Definições Swagger/OpenAPI
│   └── utils/                # Funções auxiliares (ex: criptografia)
│
├── migrations/               # Arquivos de versão do banco (Alembic)
├── instance/                 # Banco SQLite (*.db)
├── venv/                     # Ambiente virtual (não versionado)
├── .env                      # Variáveis de ambiente
├── .gitignore
├── requirements.txt
└── run.py                    # Ponto de entrada da aplicação
```

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/mathLazaro/event-anexus-back.git
cd event-anexus-back
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

Ative-o:

-   **Windows (PowerShell):**

    ```bash
    venv\Scripts\activate
    ```

-   **Linux/Mac:**
    ```bash
    source venv/bin/activate
    ```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Criar o arquivo `.env`

Crie um arquivo na raiz do projeto com o seguinte conteúdo:

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=uma_chave_super_secreta_para_flask
JWT_SECRET_KEY=uma_chave_super_secreta_para_jwt
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_aplicativo
```

> ⚠️ Obs: para testar envio de e-mails via Gmail, use uma **senha de aplicativo**, não a senha normal da conta.

---

## 🗃️ Configuração do Banco de Dados

### 1️⃣ Inicializar as migrações

```bash
flask db init
```

### 2️⃣ Criar migração

```bash
flask db migrate -m "create initial tables"
```

### 3️⃣ Aplicar migrações

```bash
flask db upgrade
```

Após isso, o arquivo `app.db` será criado dentro da pasta `instance/`.

---

## 🚀 Executando o Projeto

### 1️⃣ Rodar o servidor

```bash
flask run
```

A API estará disponível em:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📘 Documentação (Swagger)

Acesse o Swagger UI em:

👉 [http://127.0.0.1:5000/api/docs](http://127.0.0.1:5000/api/docs)

---

## 🔐 Autenticação

A autenticação utiliza **JWT (JSON Web Token)**.

Fluxo básico:

1. O usuário se cadastra (`POST /api/users`)
2. Faz login (`POST /api/auth/login`) e recebe um token JWT
3. Envia o token no cabeçalho `Authorization: Bearer <token>` nas demais rotas protegidas.

---

## 📦 Exemplo de Rotas

### Criar Usuário

`POST /api/users`

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "12345678",
    "telephone_number": "11999999999",
    "department": "Computer Science"
}
```

### Resposta

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "department": "Computer Science",
    "adm": false,
    "url": "/api/users/1"
}
```

---

## ⚡ Erros Padronizados

| Código | Tipo            | Descrição                   |
| ------ | --------------- | --------------------------- |
| 400    | `BadRequest`    | Dados inválidos ou ausentes |
| 401    | `Unauthorized`  | Token ausente ou inválido   |
| 404    | `NotFound`      | Recurso não encontrado      |
| 500    | `InternalError` | Erro interno da aplicação   |

---

## 🧠 Convenções RESTful

| Método   | Descrição                      | Exemplo Endpoint   | Retorno Esperado    |
| -------- | ------------------------------ | ------------------ | ------------------- |
| `GET`    | Obter recurso ou lista         | `/api/events`      | `200 OK`            |
| `POST`   | Criar novo recurso             | `/api/events`      | `201 Created` + URI |
| `PUT`    | Atualizar recurso inteiro      | `/api/events/{id}` | `200 OK`            |
| `PATCH`  | Atualizar parcialmente recurso | `/api/events/{id}` | `200 OK`            |
| `DELETE` | Remover recurso                | `/api/events/{id}` | `204 No Content`    |

---

## 🧹 Boas Práticas e Dicas

-   Código formatado com **Black**:

    ```bash
    black .
    ```

-   Evite versionar:

    -   `venv/`
    -   `__pycache__/`
    -   `instance/*.db`
    -   `.env`

-   Caso queira reiniciar o banco:
    ```bash
    flask db downgrade base
    flask db upgrade
    ```

---

## 👨‍💻 Autor

Desenvolvido por **Matheus Lima** 🎓  
Projeto acadêmico — disciplina de **Desenvolvimento Back-end com Python**
