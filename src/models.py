"""Modelos de dados para entrada e saída do agente de detecção de fake news."""
from typing import Optional, Literal
from pydantic import BaseModel, Field


class PostInput(BaseModel):
    """Modelo de entrada para um post a ser analisado."""
    text: str = Field(..., description="Texto do post")
    metadata: dict = Field(default_factory=dict, description="Metadados do post (curtidas, upvotes, etc.)")
    image_description: Optional[str] = Field(None, description="Descrição da imagem se houver")
    social_network: Optional[str] = Field(None, description="Rede social de origem")


class PostAnalysisInput(BaseModel):
    """Modelo completo de entrada após processamento inicial."""
    text: str
    metadata: dict
    image_description: Optional[str] = None
    social_network: Optional[str] = None
    bert_score: float = Field(..., ge=0.0, le=1.0, description="Score do BERT (0-1)")


class RiskLevel(str):
    """Níveis de risco possíveis."""
    BAIXO = "BAIXO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"
    CRITICO = "CRITICO"


class PostAnalysisOutput(BaseModel):
    """Modelo de saída estruturada da análise."""
    risk_level: Literal["BAIXO", "MEDIO", "ALTO", "CRITICO"] = Field(..., description="Nível de risco do post")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Score de risco (0-1)")
    bert_score: float = Field(..., ge=0.0, le=1.0, description="Score do BERT")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiança na classificação")
    reasoning: str = Field(..., description="Justificativa da classificação")
    relevant_sources: list[str] = Field(default_factory=list, description="Fontes confiáveis relevantes encontradas")
    factors: dict = Field(default_factory=dict, description="Fatores que influenciaram a decisão")

