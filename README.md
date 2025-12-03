# Agente de Detecção de Fake News

Sistema inteligente para detecção de fake news usando LangChain, RAG com PostgreSQL (pgvector) e classificação BERT.

## Características

- **RAG (Retrieval-Augmented Generation)**: Busca em banco vetorial com notícias de fontes confiáveis
- **Classificação BERT**: Score de fake news usando modelo BERT fine-tuned
- **Agente LangChain**: Análise inteligente combinando múltiplas fontes de informação
- **Saída Estruturada**: Resultados em formato JSON padronizado
- **Workflow Completo**: Processamento end-to-end desde JSON de entrada até classificação

## Estrutura do Projeto

```
news_agent/
├── src/
│   ├── __init__.py          # Exports principais
│   ├── main.py              # Ponto de entrada e configuração
│   ├── workflow.py          # Workflow principal
│   ├── agent.py             # Agente LangChain
│   ├── bert_classifier.py   # Classificador BERT
│   ├── vector_db.py         # RAG com pgvector
│   └── models.py            # Schemas Pydantic
├── requirements.txt
└── README.md
```

## Instalação

1. Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:

```bash
# Crie o arquivo .env na raiz do projeto
```

Conteúdo do arquivo `.env`:

```env
# Google API Key (obrigatório) - Obtenha em https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=sua-chave-aqui

# Banco Vetorial (com pgvector) - usado para RAG (obrigatório)
POSTGRES_VECTOR_DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/dbname

# Banco Normal (PostgreSQL padrão) - usado para cache de análises (obrigatório)
POSTGRES_CACHE_DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/cache_db

# Opcional: Modelo LLM a ser usado
LLM_MODEL=gemini-2.5-flash
```

**Nota:** Você pode usar dois bancos PostgreSQL separados:
- **Banco Vetorial**: PostgreSQL com extensão pgvector para busca vetorial (RAG)
- **Banco Normal**: PostgreSQL padrão para cache de análises

**Nota:** O arquivo `.env` será carregado automaticamente pelo sistema. Você também pode usar variáveis de ambiente do sistema se preferir.

3. Certifique-se de que o PostgreSQL tem a extensão pgvector instalada:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Formato de Entrada

O sistema espera um JSON com a seguinte estrutura:

```json
{
  "text": "Texto do post a ser analisado",
  "metadata": {
    "likes": 15000,
    "shares": 500,
    "comments": 200
  },
  "image_description": "Descrição da imagem (opcional)",
  "social_network": "Facebook"
}
```

## Formato de Saída

A saída é um JSON estruturado:

```json
{
  "risk_level": "CRITICO",
  "risk_score": 0.85,
  "bert_score": 0.78,
  "confidence": 0.92,
  "reasoning": "Justificativa detalhada da classificação...",
  "relevant_sources": [
    "Fonte 1",
    "Fonte 2"
  ],
  "factors": {
    "bert_score": 0.78,
    "has_image": true,
    "metadata_count": 3,
    "has_engagement": true
  }
}
```

### Níveis de Risco

- **BAIXO**: Post parece confiável
- **MEDIO**: Algumas inconsistências
- **ALTO**: Muitas inconsistências, contradiz fontes confiáveis
- **CRITICO**: Muito provável fake news

## Uso

### Uso Básico

```python
from src import analyze_post

post_json = {
    "text": "Breaking: Cientistas descobrem que vacinas causam autismo!",
    "metadata": {"likes": 15000},
    "image_description": "Imagem alarmante",
    "social_network": "Facebook"
}

result = analyze_post(post_json)
print(result)
```

### Uso Avançado (Configuração Customizada)

```python
from src import create_workflow
from src.workflow import FakeNewsWorkflow

# Cria workflow customizado
# Nota: Se pg_connection_string for fornecido, será usado para ambos os bancos
workflow = create_workflow(
    pg_connection_string="postgresql://...",  # Opcional: usa para ambos os bancos
    bert_model_name="seu-modelo-bert",
    llm_model="gemini-2.5-flash",  # ou "gemini-1.5-pro"
    google_api_key="sua-chave"
)

# Processa múltiplos posts
posts = [post1, post2, post3]
results = [workflow.process_post_json(post) for post in posts]
```

### Uso com String JSON

```python
from src import analyze_post_from_json_string

post_json_str = '{"text": "Notícia suspeita...", "metadata": {}}'
result_json = analyze_post_from_json_string(post_json_str)
```

## Componentes

### BERTClassifier

Classifica textos usando modelo BERT. Retorna score de 0 (verdadeiro) a 1 (fake news).

### VectorDB

Gerencia RAG com PostgreSQL + pgvector. Busca notícias similares de fontes confiáveis.

### FakeNewsAgent

Agente LangChain que combina:
- Score do BERT
- Resultados do RAG
- Metadados do post
- Análise de contexto

### FakeNewsWorkflow

Orquestra todo o processo:
1. Parse do JSON de entrada
2. Classificação BERT
3. Análise pelo agente
4. Geração de saída estruturada

## Configuração do Banco Vetorial

Para popular o banco vetorial com notícias confiáveis, você precisará:

1. Criar uma tabela com embeddings:

```python
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

vectorstore = PGVector(
    connection_string="postgresql://...",
    embedding_function=embeddings,
    collection_name="trusted_news"
)

# Adiciona documentos
documents = [
    Document(
        page_content="Texto da notícia confiável...",
        metadata={"source": "Fonte Confiável"}
    )
]

vectorstore.add_documents(documents)
```

## Princípios Aplicados

- **DRY (Don't Repeat Yourself)**: Código modular e reutilizável
- **KISS (Keep It Simple, Stupid)**: Interfaces simples e diretas
- **Separação de Responsabilidades**: Cada módulo tem uma função clara
- **Type Safety**: Uso de Pydantic para validação

## Modelos Gemini Disponíveis

O sistema usa o Gemini 2.5 por padrão. Modelos disponíveis:
- `gemini-2.5-flash`: Modelo rápido e eficiente (padrão)
- `gemini-2.0-flash-exp`: Modelo experimental
- `gemini-1.5-pro`: Modelo mais preciso e robusto
- `gemini-1.5-flash`: Versão mais rápida do 1.5

## Notas

- **BERT em modo de teste**: O classificador BERT está configurado para retornar scores mock (0-1) baseados em heurísticas simples. Para produção, substitua a implementação em `src/bert_classifier.py` pelo seu modelo real.
- Certifique-se de ter o PostgreSQL com pgvector configurado corretamente
- A chave da API Google (GOOGLE_API_KEY) é necessária para o agente LangChain funcionar. Obtenha em https://makersuite.google.com/app/apikey
- O Gemini 2.0 suporta structured output nativamente, garantindo respostas estruturadas confiáveis
- As variáveis de ambiente são carregadas automaticamente do arquivo `.env` na raiz do projeto

## Licença

MIT

