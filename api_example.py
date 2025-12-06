"""Exemplo de uso da API FastAPI."""
import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

# Exemplo 1: Analisar um post
print("=" * 60)
print("EXEMPLO 1: Analisar um post")
print("=" * 60)

post_data = {
    "text": "Breaking: Cientistas descobrem que vacinas causam autismo! Esta notícia foi confirmada por fontes anônimas.",
    "trend": "politics",
    "metadata": {
        "likes": 15000,
        "shares": 500,
        "comments": 200
    },
    "image_description": "Imagem de uma seringa com texto alarmante sobre vacinas",
    "social_network": "Facebook"
}

response = requests.post(f"{BASE_URL}/analyze", json=post_data)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), ensure_ascii=False, indent=2))

# Exemplo 2: Buscar posts por trend
print("\n" + "=" * 60)
print("EXEMPLO 2: Buscar posts por trend")
print("=" * 60)

response = requests.get(f"{BASE_URL}/posts/trend/politics", params={"limit": 10})
print(f"Status: {response.status_code}")
posts = response.json()
print(f"Encontrados {len(posts)} posts com trend 'politics'")
if posts:
    print("\nPrimeiro post:")
    print(json.dumps(posts[0], ensure_ascii=False, indent=2))

# Exemplo 3: Health check
print("\n" + "=" * 60)
print("EXEMPLO 3: Health check")
print("=" * 60)

response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), ensure_ascii=False, indent=2))

