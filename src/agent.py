"""Agente LangChain para análise de fake news."""
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from .models import PostAnalysisInput, PostAnalysisOutput
from .vector_db import VectorDB
from .bert_classifier import BERTClassifier

logger = logging.getLogger(__name__)


class FakeNewsAgent:
    """Agente inteligente para detecção de fake news."""
    
    def __init__(
        self,
        vector_db: VectorDB,
        bert_classifier: BERTClassifier,
        llm_model: str = "gemini-2.5-flash",
        temperature: float = 0.3
    ):
        """
        Inicializa o agente.
        
        Args:
            vector_db: Instância do VectorDB para RAG
            bert_classifier: Instância do BERTClassifier
            llm_model: Modelo LLM a ser usado (padrão: gemini-2.5-flash)
            temperature: Temperatura do LLM
        """
        self.vector_db = vector_db
        self.bert_classifier = bert_classifier
        self.llm = ChatGoogleGenerativeAI(model=llm_model, temperature=temperature)
        self._setup_tools()
    
    def _setup_tools(self):
        """Configura as ferramentas do agente."""
        # Cria funções como ferramentas
        @tool
        def buscar_noticias_similares(query: str) -> str:
            """Busca notícias confiáveis similares no banco vetorial para comparar com o post."""
            return self._search_news_tool(query)
        
        @tool
        def obter_contexto_verificacao(query: str) -> str:
            """Obtém contexto detalhado de notícias confiáveis para verificação."""
            return self._get_context_tool(query)
        
        self.tools = [buscar_noticias_similares, obter_contexto_verificacao]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    def _get_system_prompt(self) -> str:
        """Retorna o prompt do sistema para o agente."""
        return """Você é um especialista em detecção de fake news. Sua tarefa é analisar posts e determinar o nível de risco de serem fake news.

Você receberá:
1. O texto do post
2. Metadados (curtidas, upvotes, etc.)
3. Descrição da imagem (se houver)
4. Score do BERT (0-1, onde 1 = mais provável de ser fake news)

Você tem acesso a:
- Banco de dados com notícias de fontes confiáveis (use as ferramentas para buscar)
- Score do modelo BERT

Considere os seguintes fatores:
- Score do BERT (quanto maior, mais risco)
- Comparação com notícias confiáveis similares
- Metadados (posts com muitas curtidas podem ser mais perigosos se forem fake)
- Consistência entre texto e descrição da imagem
- Qualidade e credibilidade das fontes encontradas

Classifique o risco em:
- BAIXO: Post parece confiável, score BERT baixo, fontes confiáveis confirmam
- MEDIO: Algumas inconsistências, score BERT moderado
- ALTO: Muitas inconsistências, score BERT alto, contradiz fontes confiáveis
- CRITICO: Muito provável fake news, score BERT muito alto, contradições claras

Sempre forneça uma justificativa clara e detalhada."""
    
    def _search_news_tool(self, query: str) -> str:
        """Ferramenta para buscar notícias similares."""
        try:
            sources = self.vector_db.get_sources(query, k=5)
            if sources:
                return f"Fontes confiáveis encontradas: {', '.join(sources)}"
            return "Nenhuma fonte confiável similar encontrada."
        except Exception as e:
            logger.error(f"Erro na busca de notícias: {e}")
            return f"Erro ao buscar notícias: {str(e)}"
    
    def _get_context_tool(self, query: str) -> str:
        """Ferramenta para obter contexto de verificação."""
        try:
            return self.vector_db.get_context(query, k=5)
        except Exception as e:
            logger.error(f"Erro ao obter contexto: {e}")
            return f"Erro ao obter contexto: {str(e)}"
    
    def analyze(self, post_input: PostAnalysisInput) -> PostAnalysisOutput:
        """
        Analisa um post e retorna classificação estruturada.
        
        Args:
            post_input: Dados do post para análise
            
        Returns:
            Análise estruturada do post
        """
        try:
            # Busca contexto do RAG primeiro
            context = self.vector_db.get_context(post_input.text, k=5)
            sources = self.vector_db.get_sources(post_input.text, k=3)
            
            # Prepara o prompt para o LLM
            prompt = self._build_analysis_prompt(post_input, context)
            
            # Cria prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                ("human", "{input}")
            ])
            
            # Executa o LLM com structured output
            chain = prompt_template | self.llm.with_structured_output(PostAnalysisOutput)
            result = chain.invoke({"input": prompt})
            
            # Adiciona fontes relevantes
            result.relevant_sources = sources
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise do agente: {e}", exc_info=True)
            # Retorna análise padrão em caso de erro
            return self._default_analysis(post_input)
    
    def _build_analysis_prompt(self, post_input: PostAnalysisInput, context: str = "") -> str:
        """Constrói o prompt de análise para o agente."""
        prompt_parts = [
            f"Analise o seguinte post para detectar fake news:",
            f"\nTEXTO DO POST:\n{post_input.text}",
            f"\nSCORE BERT: {post_input.bert_score:.3f} (0=confiável, 1=fake news)",
        ]
        
        if context:
            prompt_parts.append(f"\nCONTEXTO DE NOTÍCIAS CONFIÁVEIS SIMILARES:\n{context}")
        
        if post_input.image_description:
            prompt_parts.append(f"\nDESCRIÇÃO DA IMAGEM:\n{post_input.image_description}")
        
        if post_input.metadata:
            prompt_parts.append(f"\nMETADADOS:")
            for key, value in post_input.metadata.items():
                prompt_parts.append(f"  - {key}: {value}")
        
        if post_input.social_network:
            prompt_parts.append(f"\nREDE SOCIAL: {post_input.social_network}")
        
        prompt_parts.append(
            "\n\nForneça sua análise estruturada considerando: "
            "- O score do BERT (quanto maior, mais risco) "
            "- A comparação com as notícias confiáveis fornecidas "
            "- Os metadados do post "
            "- A consistência entre texto e imagem "
            "- O nível de risco deve ser: BAIXO, MEDIO, ALTO ou CRITICO"
        )
        
        return "\n".join(prompt_parts)
    
    
    def _default_analysis(self, post_input: PostAnalysisInput) -> PostAnalysisOutput:
        """Retorna análise padrão em caso de erro."""
        # Calcula risco baseado apenas no BERT score
        if post_input.bert_score >= 0.8:
            risk_level = "CRITICO"
            risk_score = post_input.bert_score
        elif post_input.bert_score >= 0.6:
            risk_level = "ALTO"
            risk_score = post_input.bert_score * 0.9
        elif post_input.bert_score >= 0.4:
            risk_level = "MEDIO"
            risk_score = post_input.bert_score * 0.7
        else:
            risk_level = "BAIXO"
            risk_score = post_input.bert_score * 0.5
        
        factors = {
            "bert_score": post_input.bert_score,
            "has_image": post_input.image_description is not None,
            "metadata_count": len(post_input.metadata),
        }
        
        return PostAnalysisOutput(
            risk_level=risk_level,
            risk_score=risk_score,
            bert_score=post_input.bert_score,
            confidence=0.6,
            reasoning="Análise automática baseada no score BERT devido a erro no processamento.",
            relevant_sources=[],
            factors=factors
        )

