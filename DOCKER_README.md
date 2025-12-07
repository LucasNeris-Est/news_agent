# Executando a API com Docker

Este guia mostra como executar a API usando Docker Compose.

## Pré-requisitos

- Docker e Docker Compose instalados
- Google API Key (obtenha em https://makersuite.google.com/app/apikey)

## Configuração Rápida

1. **Crie um arquivo `.env` na raiz do projeto:**

```bash
cp env.example .env
```

2. **Edite o arquivo `.env` e adicione sua Google API Key:**

```env
GOOGLE_API_KEY=sua-chave-google-aqui
LLM_MODEL=gemini-2.5-flash  # opcional
```

3. **Inicie os serviços:**

```bash
docker-compose up -d
```

Isso irá:
- Iniciar o PostgreSQL com pgvector na porta 5433
- Iniciar a API FastAPI na porta 8000
- Configurar automaticamente as conexões de banco de dados

## Acessando a API

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Endpoints Disponíveis

### POST /analyze
Analisa um post e retorna classificação de fake news.

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Texto do post",
    "trend": "politics",
    "metadata": {"likes": 1000},
    "social_network": "Facebook"
  }'
```

### GET /posts/trend/{trend}
Retorna posts já analisados de uma tendência específica.

```bash
curl "http://localhost:8000/posts/trend/politics?limit=10"
```

### GET /health
Verifica se a API está funcionando.

```bash
curl "http://localhost:8000/health"
```

## Comandos Úteis

### Ver logs da API
```bash
docker-compose logs -f api
```

### Ver logs do PostgreSQL
```bash
docker-compose logs -f postgres
```

### Parar os serviços
```bash
docker-compose down
```

### Parar e remover volumes (limpar dados)
```bash
docker-compose down -v
```

### Reconstruir a imagem da API
```bash
docker-compose build api
docker-compose up -d api
```

## Estrutura dos Serviços

- **postgres**: Banco de dados PostgreSQL com pgvector (porta 5433)
- **api**: API FastAPI (porta 8000)

## Rede Docker

Os serviços estão na mesma rede Docker (`news_agent_network`), o que permite:

- **Comunicação interna**: A API se conecta ao PostgreSQL usando `postgres:5432` (nome do serviço)
- **Acesso externo**: A API é acessível em `localhost:8000` e o PostgreSQL em `localhost:5433`
- **Isolamento**: Os serviços estão isolados em sua própria rede

### Como funciona a conexão:

- **Dentro do Docker**: API → `postgres:5432` (nome do serviço, porta interna)
- **Fora do Docker**: Host → `localhost:8000` (API) ou `localhost:5433` (PostgreSQL)

## Notas

- A API aguarda o PostgreSQL estar saudável antes de iniciar
- As variáveis de ambiente são configuradas automaticamente no Docker Compose
- O banco de dados é inicializado automaticamente com o schema do `init_db.sql`
- Os dados do PostgreSQL são persistidos no volume `postgres_data`
- A API e o PostgreSQL estão na mesma rede Docker e podem se comunicar usando o nome do serviço

