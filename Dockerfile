FROM python:3.10-slim

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Instala dependências do sistema necessárias para o mysql-connector-python
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código fonte
COPY . .

# Copia e configura o entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Define permissões corretas
RUN chown -R appuser:appuser /app

# Muda para usuário não-root
USER appuser

# Expõe a porta que o Flask utiliza
EXPOSE 5000

# Define variáveis de ambiente para produção
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Valores padrão para as variáveis de ambiente - serão substituídos em produção
ENV DB_USER=admin
ENV DB_PASSWORD=PrimosFinCntrl2025x
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_NAME=primosfincntrl

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ping || exit 1

# Comando para iniciar a aplicação em produção (0.0.0.0 para permitir acesso externo)
ENTRYPOINT ["/app/entrypoint.sh"]
