FROM python:3.10-slim

WORKDIR /app

# Atualiza o pip primeiro
RUN pip install --upgrade pip

# Instala dependências de segurança
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configura usuário não-root
RUN useradd -m executor-user && \
    chown -R executor-user:executor-user /app && \
    chmod -R 755 /tmp

USER executor-user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]