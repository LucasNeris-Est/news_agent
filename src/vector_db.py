"""Módulo para RAG usando PostgreSQL com pgvector."""
from typing import List, Optional
import logging
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
# Import correto para versões recentes do LangChain
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class VectorDB:
    """Classe para gerenciar RAG com PostgreSQL + pgvector."""
    
    def __init__(
        self,
        connection_string: str,
        collection_name: str = "noticiasrag",
        embedding_model: str = "BAAI/bge-m3"
    ):
        """
        Inicializa o banco vetorial.
        
        Args:
            connection_string: String de conexão PostgreSQL
            collection_name: Nome da coleção/tabela
            embedding_model: Modelo de embeddings a ser usado
        """
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self.embeddings = None
        self.vectorstore = None
        self._initialize()
    
    def _initialize(self):
        """Inicializa embeddings e vectorstore."""
        try:
            logger.info(f"Carregando modelo de embeddings: {self.embedding_model_name}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
            
            logger.info("Conectando ao PostgreSQL com pgvector...")
            self.vectorstore = PGVector(
                connection_string=self.connection_string,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            logger.info("Banco vetorial inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco vetorial: {e}")
            self.vectorstore = None
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """
        Busca notícias similares no banco vetorial.
        
        Args:
            query: Texto de busca
            k: Número de resultados
            
        Returns:
            Lista de documentos similares
        """
        if self.vectorstore is None:
            logger.warning("Vectorstore não disponível. Retornando lista vazia.")
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            # Retorna apenas os documentos (sem scores)
            return [doc for doc, score in results]
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

