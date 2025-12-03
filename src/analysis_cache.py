"""Módulo para cache de análises de posts usando PostgreSQL."""
import hashlib
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import ThreadedConnectionPool

from .models import PostInput, PostAnalysisOutput

logger = logging.getLogger(__name__)


class AnalysisCache:
    """Gerencia cache de análises de posts no PostgreSQL."""
    
    def __init__(self, connection_string: str, pool_size: int = 5):
        """
        Inicializa o cache de análises.
        
        Args:
            connection_string: String de conexão PostgreSQL
            pool_size: Tamanho do pool de conexões
        """
        self.connection_string = connection_string
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Inicializa o pool de conexões."""
        try:
            self.pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                dsn=self.connection_string
            )
            logger.info("Pool de conexões PostgreSQL inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar pool de conexões: {e}")
            self.pool = None
    
    def _get_connection(self):
        """Obtém uma conexão do pool."""
        if self.pool is None:
            raise ConnectionError("Pool de conexões não inicializado")
        return self.pool.getconn()
    
    def _return_connection(self, conn):
        """Retorna uma conexão ao pool."""
        if self.pool:
            self.pool.putconn(conn)
    
    def _generate_hash(self, post_input: PostInput) -> str:
        """
        Gera hash único para um post baseado no texto e metadados principais.
        
        Args:
            post_input: Dados do post
            
        Returns:
            Hash SHA256 do post
        """
        # Cria string única baseada no texto e metadados principais
        hash_data = {
            "text": post_input.text.strip().lower(),
            "image_description": post_input.image_description.strip().lower() if post_input.image_description else "",
            "social_network": post_input.social_network or ""
        }
        
        # Serializa e gera hash
        hash_string = json.dumps(hash_data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    def get_analysis(self, post_input: PostInput) -> Optional[PostAnalysisOutput]:
        """
        Busca análise existente no cache.
        
        Args:
            post_input: Dados do post
            
        Returns:
            Análise existente ou None se não encontrada
        """
        if self.pool is None:
            return None
        
        post_hash = self._generate_hash(post_input)
        conn = None
        
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        risk_level, risk_score, bert_score, confidence,
                        reasoning, relevant_sources, factors, created_at
                    FROM post_analyses
                    WHERE post_hash = %s
                    """,
                    (post_hash,)
                )
                
                row = cur.fetchone()
                
                if row:
                    logger.info(f"Análise encontrada no cache para hash {post_hash[:8]}...")
                    return PostAnalysisOutput(
                        risk_level=row['risk_level'],
                        risk_score=float(row['risk_score']),
                        bert_score=float(row['bert_score']),
                        confidence=float(row['confidence']),
                        reasoning=row['reasoning'],
                        relevant_sources=row['relevant_sources'] or [],
                        factors=row['factors'] or {}
                    )
                
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar análise no cache: {e}")
            return None
        finally:
            if conn:
                self._return_connection(conn)
    
    def save_analysis(
        self, 
        post_input: PostInput, 
        analysis: PostAnalysisOutput
    ) -> bool:
        """
        Salva análise no cache.
        
        Args:
            post_input: Dados do post
            analysis: Resultado da análise
            
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        if self.pool is None:
            return False
        
        post_hash = self._generate_hash(post_input)
        conn = None
        
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO post_analyses (
                        post_hash, post_text, post_metadata, image_description,
                        social_network, risk_level, risk_score, bert_score,
                        confidence, reasoning, relevant_sources, factors
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (post_hash) 
                    DO UPDATE SET
                        risk_level = EXCLUDED.risk_level,
                        risk_score = EXCLUDED.risk_score,
                        bert_score = EXCLUDED.bert_score,
                        confidence = EXCLUDED.confidence,
                        reasoning = EXCLUDED.reasoning,
                        relevant_sources = EXCLUDED.relevant_sources,
                        factors = EXCLUDED.factors,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        post_hash,
                        post_input.text,
                        Json(post_input.metadata),
                        post_input.image_description,
                        post_input.social_network,
                        analysis.risk_level,
                        analysis.risk_score,
                        analysis.bert_score,
                        analysis.confidence,
                        analysis.reasoning,
                        Json(analysis.relevant_sources),
                        Json(analysis.factors)
                    )
                )
                conn.commit()
                logger.info(f"Análise salva no cache com hash {post_hash[:8]}...")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao salvar análise no cache: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                self._return_connection(conn)
    
    def close(self):
        """Fecha o pool de conexões."""
        if self.pool:
            self.pool.closeall()
            logger.info("Pool de conexões fechado")

