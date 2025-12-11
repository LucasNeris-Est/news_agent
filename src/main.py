"""Ponto de entrada principal do agente de fake news."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from .workflow import FakeNewsWorkflow
from .bert_classifier import BERTClassifier
from .vector_db import VectorDB
from .agent import FakeNewsAgent
from .analysis_cache import AnalysisCache

# Carrega variáveis de ambiente do arquivo .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    logger_temp = logging.getLogger(__name__)
    logger_temp.info(f"Variáveis de ambiente carregadas de {env_path}")
else:
    # Tenta carregar do diretório raiz do projeto
    root_env = Path(__file__).parent.parent.parent / ".env"
    if root_env.exists():
        load_dotenv(root_env)
    else:
        # Carrega do diretório atual
        load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_workflow(
    pg_connection_string: Optional[str] = None,
    bert_model_name: Optional[str] = None,
    llm_model: str = "gemini-2.5-flash",
    google_api_key: Optional[str] = None,
    embedding_model: Optional[str] = None,
    enable_cache: bool = True
) -> FakeNewsWorkflow:
    """
    Cria e configura o workflow completo.
    
    Args:
        pg_connection_string: String de conexão PostgreSQL. 
                             Se fornecido, será usado para ambos os bancos (vetorial e cache).
                             Se None, usa variáveis de ambiente:
                             - POSTGRES_VECTOR_DB_CONNECTION_STRING (banco vetorial com pgvector)
                             - POSTGRES_CACHE_DB_CONNECTION_STRING (banco normal para cache)
                             Fallback para POSTGRES_CONNECTION_STRING se as novas variáveis não existirem.
        bert_model_name: Nome do modelo BERT. Se None, usa padrão
        llm_model: Modelo LLM a ser usado (padrão: gemini-2.5-flash)
        google_api_key: Chave da API Google. Se None, usa variável de ambiente GOOGLE_API_KEY
        embedding_model: Modelo de embeddings. Se None, usa BAAI/bge-m3 ou variável EMBEDDING_MODEL
        enable_cache: Se True, habilita cache de análises no PostgreSQL
        
    Returns:
        Instância configurada do FakeNewsWorkflow
    """
    # Configura Google API key (prioridade: parâmetro > .env > variável de ambiente)
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key
    elif not os.getenv("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY não configurada. Configure no arquivo .env ou variável de ambiente.")
    
    # Configura conexão PostgreSQL para banco vetorial (prioridade: parâmetro > .env > variável de ambiente)
    # Se pg_connection_string for fornecido, usa para ambos os bancos (compatibilidade)
    if pg_connection_string:
        vector_db_conn = pg_connection_string
        cache_db_conn = pg_connection_string
    else:
        vector_db_conn = os.getenv("POSTGRES_VECTOR_DB_CONNECTION_STRING")
        cache_db_conn = os.getenv("POSTGRES_CACHE_DB_CONNECTION_STRING")
        
        # Fallback para variável antiga (compatibilidade)
        if not vector_db_conn:
            vector_db_conn = os.getenv("POSTGRES_CONNECTION_STRING")
        if not cache_db_conn:
            cache_db_conn = os.getenv("POSTGRES_CONNECTION_STRING")
    
    if not vector_db_conn:
        logger.warning("POSTGRES_VECTOR_DB_CONNECTION_STRING não configurada. RAG pode não funcionar.")
        logger.warning("Configure POSTGRES_VECTOR_DB_CONNECTION_STRING no arquivo .env")
        vector_db_conn = "postgresql://user:password@localhost:5432/dbname"
    
    if not cache_db_conn:
        logger.warning("POSTGRES_CACHE_DB_CONNECTION_STRING não configurada. Cache pode não funcionar.")
        logger.warning("Configure POSTGRES_CACHE_DB_CONNECTION_STRING no arquivo .env")
        cache_db_conn = "postgresql://user:password@localhost:5432/dbname"
    
    # Configura modelo de embeddings (prioridade: parâmetro > .env > padrão)
    embedding_model_name = embedding_model or os.getenv("EMBEDDING_MODEL") or "BAAI/bge-m3"
    
    # Configura modelo BERT (prioridade: parâmetro > padrão)
    bert_model = bert_model_name or "vzani/portuguese-fake-news-classifier-bertimbau-fake-br"
    
    # Inicializa componentes
    logger.info("Inicializando componentes...")
    logger.info(f"Usando modelo de embeddings: {embedding_model_name}")
    logger.info(f"Usando modelo BERT: {bert_model}")
    bert_classifier = BERTClassifier(model_name=bert_model)
    vector_db = VectorDB(connection_string=vector_db_conn, embedding_model=embedding_model_name)
    agent = FakeNewsAgent(
        vector_db=vector_db,
        bert_classifier=bert_classifier,
        llm_model=llm_model
    )
    
    # Inicializa cache de análises
    analysis_cache = None
    if enable_cache:
        try:
            analysis_cache = AnalysisCache(connection_string=cache_db_conn)
            logger.info("Cache de análises habilitado")
        except Exception as e:
            logger.warning(f"Erro ao inicializar cache: {e}. Continuando sem cache.")
    
    # Cria workflow
    workflow = FakeNewsWorkflow(
        vector_db=vector_db,
        bert_classifier=bert_classifier,
        agent=agent,
        analysis_cache=analysis_cache
    )
    
    logger.info("Workflow criado com sucesso!")
    return workflow


def analyze_post(
    post_json: Dict[str, Any],
    workflow: Optional[FakeNewsWorkflow] = None
) -> Dict[str, Any]:
    """
    Função principal para analisar um post.
    
    Args:
        post_json: Dicionário com dados do post
        workflow: Workflow pré-configurado. Se None, cria um novo
        
    Returns:
        Dicionário com análise estruturada
    """
    if workflow is None:
        workflow = create_workflow()
    
    return workflow.process_post_json(post_json)


def analyze_post_from_json_string(
    post_json_str: str,
    workflow: Optional[FakeNewsWorkflow] = None
) -> str:
    """
    Analisa um post a partir de uma string JSON.
    
    Args:
        post_json_str: String JSON com dados do post
        workflow: Workflow pré-configurado. Se None, cria um novo
        
    Returns:
        String JSON com análise estruturada
    """
    if workflow is None:
        workflow = create_workflow()
    
    return workflow.process_post_json_string(post_json_str)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de post JSON
    example_post = {
        "text": "Breaking: Cientistas descobrem que vacinas causam autismo!",
        "metadata": {
            "likes": 15000,
            "shares": 500,
            "comments": 200
        },
        "image_description": "Imagem de uma seringa com texto alarmante",
        "social_network": "Facebook"
    }
    
    # Analisa o post
    result = analyze_post(example_post)
    
    # Imprime resultado
    print(json.dumps(result, ensure_ascii=False, indent=2))

