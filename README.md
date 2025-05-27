Chatbot API

API desenvolvida em Python (FastAPI) para um chatbot inteligente com:

    Autenticação via JWT

    Persistência de contexto com PostgreSQL via Supabase

    Estrutura modular

    Simulação de integração com OpenAI

Funcionalidades

    Autenticação via token JWT

    Endpoint /ask com contexto baseado nas últimas 5 interações

    Armazenamento de usuários e chats no PostgreSQL (Supabase)

    Simulação de resposta estilo agente inteligente

    Estrutura pronta para integração real com OpenAI

Tecnologias Utilizadas

    FastAPI

    SQLAlchemy

    PostgreSQL / Supabase

    Pydantic

    Python-Jose (JWT)

    Uvicorn (servidor ASGI)

    OpenAI SDK (simulado)

Instalação e Execução Local
1. Clone o repositório

git clone https://github.com/hiluey/chatbot.git
cd chatbot_api

2. Crie o ambiente virtual e ative

python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure o .env

Crie um arquivo .env na raiz, com base no .env.example:

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/YOUR_DB
OPENAI_API_KEY=sk-...
JWT_SECRET=su...

5. Crie as tabelas no banco

python -m app.create_tables

6. Rode o servidor

uvicorn app.main:app --reload

Endpoints
POST /signup

    Criar um novo usuário

    Body JSON:

{
  "username": "giovanna",
  "password": "123456"
}

POST /token

    Obter o token JWT

    Body: x-www-form-urlencoded

username=giovanna
password=123456

POST /v1/ask

    Envia uma pergunta

    Header:

Authorization: Bearer <token>

    Body JSON:

{
  "question": "Qual é a capital da França?"
}

    Resposta:

{
    "id": 5,
    "question": "Qual é a capital da França?",
    "answer": "A capital da França é Paris.",
    "timestamp": "2025-05-26T17:45:10.049959"
}


Feito por: Giovanna Hiluey
# chat_bot
# chatbot
