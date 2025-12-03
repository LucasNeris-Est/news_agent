# Docker Setup - News Agent

Este projeto inclui configuração Docker para facilitar o desenvolvimento e deploy.

## Estrutura

- **docker-compose.yml**: Configuração do PostgreSQL com pgvector
- **Dockerfile**: Imagem Docker para a aplicação (opcional)
- **init_db.sql**: Script SQL para inicializar o banco de dados

## Como usar

### 1. Iniciar o banco de dados PostgreSQL

```bash
docker-compose up -d
```

Isso irá:
- Criar um container PostgreSQL com pgvector
- Executar o script `init_db.sql` automaticamente
- Criar a tabela `post_analyses` para cache de análises
- Configurar índices e triggers

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` baseado no `env.example`:

```env
GOOGLE_API_KEY=sua-chave-aqui
POSTGRES_CONNECTION_STRING=postgresql://news_agent:news_agent_password@localhost:5432/news_agent_db
```

**Nota**: Se estiver usando Docker, use `localhost` para conexão externa. Se estiver dentro do container, use `postgres` como host.

### 3. Verificar se o banco está rodando

```bash
docker-compose ps
```

### 4. Parar o banco de dados

```bash
docker-compose down
```

Para remover também os volumes (dados):

```bash
docker-compose down -v
```

## Estrutura do Banco de Dados

### Tabela `post_analyses`

Armazena análises de posts com os seguintes campos:

- `id`: ID único (serial)
- `post_hash`: Hash SHA256 do post (único, usado para evitar duplicatas)
- `post_text`: Texto do post
- `post_metadata`: Metadados em JSONB
- `image_description`: Descrição da imagem (se houver)
- `social_network`: Rede social de origem
- `risk_level`: Nível de risco (BAIXO, MEDIO, ALTO, CRITICO)
- `risk_score`: Score de risco (0-1)
- `bert_score`: Score do BERT (0-1)
- `confidence`: Confiança na classificação (0-1)
- `reasoning`: Justificativa da análise
- `relevant_sources`: Fontes relevantes (JSONB)
- `factors`: Fatores que influenciaram (JSONB)
- `created_at`: Data de criação
- `updated_at`: Data de atualização (atualizado automaticamente)

### Índices

- `idx_post_hash`: Busca rápida por hash
- `idx_created_at`: Busca por data
- `idx_risk_level`: Busca por nível de risco

## Cache de Análises

O sistema usa hash SHA256 do texto do post + metadados principais para identificar posts únicos. Posts já analisados são recuperados do cache automaticamente, evitando reprocessamento.

### Como funciona

1. Quando um post é analisado, um hash é gerado baseado em:
   - Texto do post (normalizado)
   - Descrição da imagem (se houver)
   - Rede social

2. O sistema verifica se já existe uma análise com esse hash

3. Se existir, retorna a análise do cache (muito mais rápido)

4. Se não existir, processa e salva no banco

## Comandos Úteis

### Ver logs do PostgreSQL

```bash
docker-compose logs postgres
```

### Conectar ao banco via psql

```bash
docker-compose exec postgres psql -U news_agent -d news_agent_db
```

### Verificar análises salvas

```sql
SELECT post_hash, risk_level, risk_score, created_at 
FROM post_analyses 
ORDER BY created_at DESC 
LIMIT 10;
```

### Limpar cache (cuidado!)

```sql
TRUNCATE TABLE post_analyses;
```

## Troubleshooting

### Erro de conexão

Verifique se o container está rodando:
```bash
docker-compose ps
```

### Erro de permissão

Certifique-se de que o usuário e senha no `.env` correspondem ao `docker-compose.yml`:
- Usuário: `news_agent`
- Senha: `news_agent_password`
- Banco: `news_agent_db`

### Porta já em uso

Se a porta 5432 já estiver em uso, altere no `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use outra porta
```

E atualize o `POSTGRES_CONNECTION_STRING` no `.env` para usar a nova porta.

