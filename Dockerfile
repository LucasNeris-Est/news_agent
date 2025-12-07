FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY src/ ./src/
COPY run_api.py ./

# Expõe porta da API
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

