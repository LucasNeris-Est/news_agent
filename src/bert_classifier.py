"""Módulo para classificação usando modelo BERT fine-tuned para fake news em português."""
import logging
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline
)

logger = logging.getLogger(__name__)


class BERTClassifier:
    """Classificador BERT para fake news usando modelo fine-tuned em português."""
    
    def __init__(self, model_name: str = "vzani/portuguese-fake-news-classifier-bertimbau-fake-br"):
        """
        Inicializa o classificador BERT com modelo do Hugging Face.
        
        Args:
            model_name: Nome do modelo no Hugging Face (padrão: bertimbau-fake-br)
        """
        try:
            logger.info(f"Carregando modelo BERT: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer
            )
            logger.info("BERTClassifier inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo BERT: {e}")
            raise
    
    def classify(self, text: str) -> float:
        """
        Classifica um texto e retorna score de fake news (0-1).
        
        O modelo retorna:
        - LABEL_0: Fake news (score de fake news = score do modelo)
        - LABEL_1: True news (score de fake news = 1 - score do modelo)
        
        Args:
            text: Texto a ser classificado
            
        Returns:
            Score de fake news entre 0 (verdadeiro) e 1 (fake news)
        """
        try:
            # A pipeline do transformers já faz truncamento automaticamente,
            # mas vamos garantir que o texto seja truncado corretamente
            # Usa o tokenizer para truncar o texto antes de passar para a pipeline
            tokens = self.tokenizer.encode(
                text,
                add_special_tokens=True,
                max_length=512,
                truncation=True,
                return_tensors=None
            )
            # Decodifica de volta para texto (já truncado corretamente)
            truncated_text = self.tokenizer.decode(tokens, skip_special_tokens=True)
            
            # Classifica o texto truncado
            result = self.classifier(truncated_text)[0]
            
            # O modelo retorna LABEL_0 para fake news e LABEL_1 para true news
            # score é a confiança na predição
            if result["label"] == "LABEL_0":  # Fake news
                fake_score = result["score"]
            else:  # LABEL_1 - True news
                fake_score = 1.0 - result["score"]
            
            # Garante que o score está entre 0 e 1
            fake_score = max(0.0, min(1.0, fake_score))
            
            logger.debug(f"BERT score calculado: {fake_score:.3f} (label: {result['label']}, confidence: {result['score']:.3f})")
            return round(fake_score, 3)
            
        except Exception as e:
            logger.error(f"Erro ao classificar texto: {e}")
            # Retorna score neutro em caso de erro
            return 0.5

