"""Exemplo de uso do agente de detecção de fake news."""
import json
from src import analyze_post, create_workflow

# Exemplo 1: Uso simples
print("=" * 60)
print("EXEMPLO 1: Uso Simples")
print("=" * 60)

post_json = {
    "text": "Breaking: Cientistas descobrem que vacinas causam autismo! Esta notícia foi confirmada por fontes anônimas.",
    "metadata": {
        "likes": 15000,
        "shares": 500,
        "comments": 200
    },
    "image_description": "Imagem de uma seringa com texto alarmante sobre vacinas",
    "social_network": "Facebook"
}

result = analyze_post(post_json)
print(json.dumps(result, ensure_ascii=False, indent=2))

# Exemplo 2: Post com baixo risco
print("\n" + "=" * 60)
print("EXEMPLO 2: Post com Baixo Risco")
print("=" * 60)

post_json_2 = {
    "text": "A Organização Mundial da Saúde anunciou hoje novas diretrizes para vacinação contra COVID-19.",
    "metadata": {
        "likes": 500,
        "shares": 50
    },
    "social_network": "Twitter"
}

result_2 = analyze_post(post_json_2)
print(json.dumps(result_2, ensure_ascii=False, indent=2))

# Exemplo 3: Uso com workflow customizado
print("\n" + "=" * 60)
print("EXEMPLO 3: Workflow Customizado")
print("=" * 60)

# Cria workflow com configurações customizadas
workflow = create_workflow(
    pg_connection_string="postgresql://user:password@localhost:5432/news_db",
    llm_model="gemini-2.5-flash"  # ou "gemini-1.5-pro" para mais precisão
)

post_json_3 = {
    "text": "URGENTE: Governo esconde verdade sobre alienígenas!",
    "metadata": {
        "upvotes": 5000,
        "comments": 1000
    },
    "image_description": "Foto de OVNI não identificado",
    "social_network": "Reddit"
}

result_3 = workflow.process_post_json(post_json_3)
print(json.dumps(result_3, ensure_ascii=False, indent=2))

