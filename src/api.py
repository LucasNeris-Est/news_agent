"""API FastAPI para análise de fake news."""
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List, Optional
import logging

from .main import create_workflow
from .workflow import FakeNewsWorkflow

logger = logging.getLogger(__name__)

# Cria instância do FastAPI
app = FastAPI(
    title="Fake News Detection API",
    description="API para análise de posts e detecção de fake news",
    version="1.0.0"
)

# Workflow global (inicializado na startup)
workflow: Optional[FakeNewsWorkflow] = None


@app.on_event("startup")
async def startup_event():
    """Inicializa o workflow na startup da API."""
    global workflow
    try:
        workflow = create_workflow()
        logger.info("API iniciada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar workflow: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpa recursos na shutdown da API."""
    global workflow
    if workflow and workflow.analysis_cache:
        workflow.analysis_cache.close()
    logger.info("API encerrada")


@app.post("/analyze")
async def analyze_post(post_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analisa um post e retorna a classificação de fake news.
    
    Body:
        - text: Texto do post (obrigatório)
        - metadata: Metadados do post (opcional)
        - image_description: Descrição da imagem (opcional)
        - social_network: Rede social de origem (opcional)
        - trend: Tendência/categoria do post (opcional)
    
    Returns:
        Análise estruturada com risk_level, risk_score, bert_score, etc.
    """
    if workflow is None:
        raise HTTPException(status_code=503, detail="Workflow não inicializado")
    
    try:
        result = workflow.process_post_json(post_json)
        return result
    except Exception as e:
        logger.error(f"Erro ao analisar post: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao processar post: {str(e)}")


@app.get("/posts/trend/{trend}")
async def get_posts_by_trend(trend: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Retorna lista de posts já analisados de uma tendência específica.
    
    Args:
        trend: Tendência/categoria a buscar
        limit: Número máximo de resultados (padrão: 100, máximo: 1000)
    
    Returns:
        Lista de posts analisados com a tendência especificada
    """
    if workflow is None or workflow.analysis_cache is None:
        raise HTTPException(status_code=503, detail="Cache não disponível")
    
    # Limita o máximo de resultados
    limit = min(limit, 1000)
    
    try:
        posts = workflow.analysis_cache.get_posts_by_trend(trend, limit)
        return posts
    except Exception as e:
        logger.error(f"Erro ao buscar posts por trend: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar posts: {str(e)}")


@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int) -> Dict[str, Any]:
    """
    Retorna uma análise específica por ID.
    
    Args:
        post_id: ID da análise
    
    Returns:
        Dados completos da análise
    """
    if workflow is None or workflow.analysis_cache is None:
        raise HTTPException(status_code=503, detail="Cache não disponível")
    
    try:
        post = workflow.analysis_cache.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail=f"Análise com ID {post_id} não encontrada")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar post por ID: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar post: {str(e)}")


@app.get("/posts")
async def get_posts(page: int = 1, limit: int = 20) -> Dict[str, Any]:
    """
    Retorna lista paginada de análises.
    
    Args:
        page: Número da página (começa em 1, padrão: 1)
        limit: Número de resultados por página (padrão: 20, máximo: 100)
    
    Returns:
        Dicionário com 'data' (lista de posts), 'total', 'page', 'limit', 'pages'
    """
    if workflow is None or workflow.analysis_cache is None:
        raise HTTPException(status_code=503, detail="Cache não disponível")
    
    try:
        result = workflow.analysis_cache.get_posts_paginated(page, limit)
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar posts paginados: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar posts: {str(e)}")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Endpoint de health check."""
    return {"status": "ok", "service": "fake-news-detection-api"}

