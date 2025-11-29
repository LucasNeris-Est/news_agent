"""Workflow principal para processamento de posts."""
import json
import logging
from typing import Dict, Any

from .models import PostInput, PostAnalysisInput, PostAnalysisOutput
from .bert_classifier import BERTClassifier
from .vector_db import VectorDB
from .agent import FakeNewsAgent

logger = logging.getLogger(__name__)


class FakeNewsWorkflow:
    """Workflow completo para análise de fake news."""
    
    def __init__(
        self,
        vector_db: VectorDB,
        bert_classifier: BERTClassifier,
        agent: FakeNewsAgent
    ):
        """
        Inicializa o workflow.
        
        Args:
            vector_db: Instância do VectorDB
            bert_classifier: Instância do BERTClassifier
            agent: Instância do FakeNewsAgent
        """
        self.vector_db = vector_db
        self.bert_classifier = bert_classifier
        self.agent = agent
    
    def process_post_json(self, post_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa um post em formato JSON e retorna análise estruturada.
        
        Args:
            post_json: Dicionário com dados do post
            
        Returns:
            Dicionário com análise estruturada
        """
        try:
            # 1. Parse do JSON de entrada
            post_input = self._parse_post_json(post_json)
            
            # 2. Classificação BERT
            bert_score = self.bert_classifier.classify(post_input.text)
            logger.info(f"Score BERT: {bert_score:.3f}")
            
            # 3. Cria entrada completa para o agente
            analysis_input = PostAnalysisInput(
                text=post_input.text,
                metadata=post_input.metadata,
                image_description=post_input.image_description,
                social_network=post_input.social_network,
                bert_score=bert_score
            )
            
            # 4. Análise pelo agente
            analysis_output = self.agent.analyze(analysis_input)
            
            # 5. Converte saída para JSON
            return self._output_to_dict(analysis_output)
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}", exc_info=True)
            return self._error_output(str(e))
    
    def process_post_json_string(self, post_json_str: str) -> str:
        """
        Processa um post em formato JSON string e retorna análise em JSON string.
        
        Args:
            post_json_str: String JSON com dados do post
            
        Returns:
            String JSON com análise estruturada
        """
        post_json = json.loads(post_json_str)
        result = self.process_post_json(post_json)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _parse_post_json(self, post_json: Dict[str, Any]) -> PostInput:
        """Parseia JSON de entrada para PostInput."""
        return PostInput(
            text=post_json.get("text", ""),
            metadata=post_json.get("metadata", {}),
            image_description=post_json.get("image_description"),
            social_network=post_json.get("social_network")
        )
    
    def _output_to_dict(self, output: PostAnalysisOutput) -> Dict[str, Any]:
        """Converte PostAnalysisOutput para dicionário."""
        return {
            "risk_level": output.risk_level,
            "risk_score": round(output.risk_score, 3),
            "bert_score": round(output.bert_score, 3),
            "confidence": round(output.confidence, 3),
            "reasoning": output.reasoning,
            "relevant_sources": output.relevant_sources,
            "factors": output.factors
        }
    
    def _error_output(self, error_message: str) -> Dict[str, Any]:
        """Retorna saída de erro estruturada."""
        return {
            "error": True,
            "error_message": error_message,
            "risk_level": "MEDIO",  # Default conservador
            "risk_score": 0.5,
            "bert_score": 0.5,
            "confidence": 0.0,
            "reasoning": f"Erro no processamento: {error_message}",
            "relevant_sources": [],
            "factors": {}
        }

