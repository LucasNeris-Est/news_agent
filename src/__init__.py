"""Agente de detecção de fake news com LangChain e RAG."""
from .main import (
    create_workflow,
    analyze_post,
    analyze_post_from_json_string
)
from .models import (
    PostInput,
    PostAnalysisInput,
    PostAnalysisOutput
)
from .workflow import FakeNewsWorkflow
from .agent import FakeNewsAgent
from .bert_classifier import BERTClassifier
from .vector_db import VectorDB
from .analysis_cache import AnalysisCache

__all__ = [
    "create_workflow",
    "analyze_post",
    "analyze_post_from_json_string",
    "PostInput",
    "PostAnalysisInput",
    "PostAnalysisOutput",
    "FakeNewsWorkflow",
    "FakeNewsAgent",
    "BERTClassifier",
    "VectorDB",
    "AnalysisCache"
]

