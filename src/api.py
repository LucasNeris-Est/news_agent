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


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Endpoint de health check."""
    return {"status": "ok", "service": "fake-news-detection-api"}

