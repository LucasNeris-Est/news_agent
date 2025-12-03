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
COPY *.py ./

# Expõe porta (se necessário para API futura)
EXPOSE 8000

# Comando padrão
CMD ["python", "example_usage.py"]

