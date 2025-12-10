"""Módulo para RAG usando PostgreSQL com pgvector."""
from typing import List, Optional
import logging
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from langchain_community.embeddings import HuggingFaceEmbeddings
# Import correto para versões recentes do LangChain
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class VectorDB:
    """Classe para gerenciar RAG com PostgreSQL + pgvector usando tabela customizada."""
    
    def __init__(
        self,
        connection_string: str,
        collection_name: str = "noticiasrag",
        embedding_model: str = "BAAI/bge-m3",
        table_name: str = "noticiasrag"
    ):
        """
        Inicializa o banco vetorial.
        
        Args:
            connection_string: String de conexão PostgreSQL
            collection_name: Nome da coleção (mantido para compatibilidade)
            embedding_model: Modelo de embeddings a ser usado
            table_name: Nome da tabela no banco (padrão: noticiasrag)
        """
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.table_name = table_name
        self.embedding_model_name = embedding_model
        self.embeddings = None
        self._initialize()
    
    def _initialize(self):
        """Inicializa embeddings e conexão."""
        try:
            logger.info(f"Carregando modelo de embeddings: {self.embedding_model_name}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
            
            logger.info(f"Conectando ao PostgreSQL com pgvector usando tabela '{self.table_name}'...")
            # Testa conexão
            conn = psycopg2.connect(self.connection_string)
            conn.close()
            logger.info("Banco vetorial inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco vetorial: {e}")
            self.embeddings = None
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """
        Busca notícias similares no banco vetorial usando a tabela noticiasrag.
        
        Args:
            query: Texto de busca
            k: Número de resultados
            
        Returns:
            Lista de documentos similares
        """
        if self.embeddings is None:
            logger.warning("Embeddings não disponíveis. Retornando lista vazia.")
            return []
        
        try:
            # Gera embedding da query
            query_embedding = self.embeddings.embed_query(query)
            
            # Conecta ao banco e faz busca vetorial
            conn = psycopg2.connect(self.connection_string)
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Converte embedding para string no formato do PostgreSQL
                    embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
                    
                    # Busca usando cosine similarity (operador <=> retorna distância)
                    cur.execute(f"""
                        SELECT 
                            id,
                            document,
                            metadata,
                            1 - (embedding <=> %s::vector) as similarity
                        FROM {self.table_name}
                        WHERE embedding IS NOT NULL
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (embedding_str, embedding_str, k))
                    
                    results = cur.fetchall()
                    
                    documents = []
                    for row in results:
                        # Converte metadata para dict se necessário
                        metadata = row['metadata']
                        if isinstance(metadata, str):
                            metadata = json.loads(metadata)
                        elif metadata is None:
                            metadata = {}
                        
                        doc = Document(
                            page_content=row['document'] or '',
                            metadata=metadata
                        )
                        documents.append(doc)
                    
                    return documents
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"Erro na busca vetorial: {e}")
            return []
    
    def get_context(self, query: str, k: int = 5) -> str:
        """
        Obtém contexto formatado de notícias similares.
        
        Args:
            query: Texto de busca
            k: Número de resultados
            
        Returns:
            Contexto formatado como string
        """
        documents = self.search_similar(query, k)
        
        if not documents:
            return "Nenhuma notícia confiável similar encontrada no banco de dados."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content
            metadata = doc.metadata
            source = metadata.get("source", "Fonte desconhecida")
            context_parts.append(f"[Fonte {i}: {source}]\n{content}\n")
        
        return "\n".join(context_parts)
    
    def get_sources(self, query: str, k: int = 5) -> List[str]:
        """
        Obtém lista de fontes confiáveis encontradas.
        
        Args:
            query: Texto de busca
            k: Número de resultados
            
        Returns:
            Lista de fontes
        """
        documents = self.search_similar(query, k)
        sources = []
        seen = set()
        
        for doc in documents:
            source = doc.metadata.get("source", "Fonte desconhecida")
            if source not in seen:
                sources.append(source)
                seen.add(source)
        
        return sources
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Adiciona documentos à tabela noticiasrag.
        
        Args:
            documents: Lista de documentos para adicionar
            
        Returns:
            Lista de IDs dos documentos inseridos
        """
        if self.embeddings is None:
            logger.warning("Embeddings não disponíveis. Não é possível adicionar documentos.")
            return []
        
        try:
            conn = psycopg2.connect(self.connection_string)
            inserted_ids = []
            try:
                with conn.cursor() as cur:
                    for doc in documents:
                        # Gera embedding do documento
                        embedding = self.embeddings.embed_query(doc.page_content)
                        embedding_str = '[' + ','.join(map(str, embedding)) + ']'
                        
                        # Converte metadata para JSON
                        metadata_json = json.dumps(doc.metadata) if doc.metadata else '{}'
                        
                        # Insere na tabela
                        cur.execute(f"""
                            INSERT INTO {self.table_name} (document, metadata, embedding)
                            VALUES (%s, %s::jsonb, %s::vector)
                            RETURNING id
                        """, (doc.page_content, metadata_json, embedding_str))
                        
                        result = cur.fetchone()
                        if result:
                            inserted_ids.append(str(result[0]))
                    
                    conn.commit()
                    logger.info(f"{len(inserted_ids)} documentos adicionados à tabela {self.table_name}")
                    return inserted_ids
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {e}")
            return []
    
    @property
    def vectorstore(self):
        """
        Propriedade para compatibilidade com código que usa vectorstore.
        Retorna self para permitir chamadas como vectorstore.add_documents()
        """
        return self

