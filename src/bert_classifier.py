"""Módulo para classificação usando modelo BERT (versão de teste)."""
import logging
import hashlib

logger = logging.getLogger(__name__)


class BERTClassifier:
    """Classificador BERT para fake news (versão de teste - retorna score mock)."""
    
    def __init__(self, model_name=None):
        """
        Inicializa o classificador BERT (versão de teste).
        
        Args:
            model_name: Ignorado na versão de teste, mantido para compatibilidade
        """
        logger.info("BERTClassifier inicializado em modo de teste (mock)")
    
    def classify(self, text: str) -> float:
        """
        Classifica um texto e retorna score de fake news (0-1).
        Versão de teste: retorna score baseado em heurísticas simples.
        
        Args:
            text: Texto a ser classificado
            
        Returns:
            Score de fake news entre 0 (verdadeiro) e 1 (fake news)
        """
        # Simula um score baseado em palavras-chave comuns de fake news
        fake_keywords = [
            "falso", "mentira", "fake", "notícia falsa", "boato", 
            "urgente", "breaking", "descobrem", "escondem", "revelação",
            "governo esconde", "cientistas descobrem", "médicos alertam"
        ]
        
        text_lower = text.lower()
        
        # Conta palavras-chave suspeitas
        matches = sum(1 for keyword in fake_keywords if keyword in text_lower)
        
        # Calcula score baseado em keywords (0.2 a 0.8)
        base_score = 0.2 + (matches * 0.15)
        
        # Adiciona variação baseada no hash do texto para simular comportamento real
        text_hash = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        variation = (text_hash % 20) / 100.0  # Variação de 0 a 0.2
        
        final_score = min(base_score + variation, 0.95)
        final_score = max(final_score, 0.1)  # Mínimo de 0.1
        
        logger.debug(f"BERT score calculado: {final_score:.3f} (matches: {matches})")
        return round(final_score, 3)

