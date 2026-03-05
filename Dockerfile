# Dockerfile Sênior para Ecossistema MoveMind
FROM python:3.12-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema (FFmpeg para Projeto 15 e LibPQ para Postgres)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do servidor
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para iniciar o servidor com Uvicorn (Ajustado para o path correto)
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
