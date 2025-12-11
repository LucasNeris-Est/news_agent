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
            "social_network": post_input.social_network or "",
            "trend": post_input.trend or ""
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
                        social_network, trend, risk_level, risk_score, bert_score,
                        confidence, reasoning, relevant_sources, factors
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                        post_input.trend,
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
    
    def get_distinct_trends(self) -> list[str]:
        """
        Retorna lista de trends distintas presentes no banco.
        
        Returns:
            Lista de trends distintas (ordenadas alfabeticamente)
        """
        if self.pool is None:
            logger.warning("Pool de conexões não disponível")
            return []
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT DISTINCT trend
                    FROM post_analyses
                    WHERE trend IS NOT NULL AND trend != ''
                    ORDER BY trend ASC
                """)
                
                results = cur.fetchall()
                trends = [row['trend'] for row in results]
                return trends
        except Exception as e:
            logger.error(f"Erro ao buscar trends distintas: {e}")
            return []
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_posts_by_trend(self, trend: str, limit: int = 100) -> list[Dict[str, Any]]:
        """
        Busca posts analisados por tendência.
        
        Args:
            trend: Tendência/categoria a buscar
            limit: Número máximo de resultados (padrão: 100)
            
        Returns:
            Lista de posts analisados com a tendência especificada
        """
        if self.pool is None:
            return []
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        id, post_hash, post_text, post_metadata, image_description,
                        social_network, trend, risk_level, risk_score,
                        bert_score, confidence, reasoning, relevant_sources,
                        factors, created_at, updated_at
                    FROM post_analyses
                    WHERE trend = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (trend, limit)
                )
                
                rows = cur.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar posts por trend: {e}")
            return []
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca uma análise específica por ID.
        
        Args:
            post_id: ID da análise
            
        Returns:
            Dicionário com os dados da análise ou None se não encontrado
        """
        if self.pool is None:
            return None
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        id, post_hash, post_text, post_metadata, image_description,
                        social_network, trend, risk_level, risk_score,
                        bert_score, confidence, reasoning, relevant_sources,
                        factors, created_at, updated_at
                    FROM post_analyses
                    WHERE id = %s
                    """,
                    (post_id,)
                )
                
                row = cur.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Erro ao buscar post por ID: {e}")
            return None
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_posts_paginated(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        Busca análises com paginação.
        
        Args:
            page: Número da página (começa em 1)
            limit: Número de resultados por página (padrão: 20, máximo: 100)
            
        Returns:
            Dicionário com 'data' (lista de posts), 'total', 'page', 'limit', 'pages'
        """
        if self.pool is None:
            return {"data": [], "total": 0, "page": page, "limit": limit, "pages": 0}
        
        # Valida e limita o limit
        limit = min(max(1, limit), 100)
        page = max(1, page)
        offset = (page - 1) * limit
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Conta total de registros
                cur.execute("SELECT COUNT(*) as total FROM post_analyses")
                total = cur.fetchone()['total']
                
                # Busca registros paginados
                cur.execute(
                    """
                    SELECT 
                        id, post_hash, post_text, post_metadata, image_description,
                        social_network, trend, risk_level, risk_score,
                        bert_score, confidence, reasoning, relevant_sources,
                        factors, created_at, updated_at
                    FROM post_analyses
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
                
                rows = cur.fetchall()
                data = [dict(row) for row in rows]
                pages = (total + limit - 1) // limit  # Arredonda para cima
                
                return {
                    "data": data,
                    "total": total,
                    "page": page,
                    "limit": limit,
                    "pages": pages
                }
                
        except Exception as e:
            logger.error(f"Erro ao buscar posts paginados: {e}")
            return {"data": [], "total": 0, "page": page, "limit": limit, "pages": 0}
        finally:
            if conn:
                self._return_connection(conn)
    
    def close(self):
        """Fecha o pool de conexões."""
        if self.pool:
            self.pool.closeall()
            logger.info("Pool de conexões fechado")

