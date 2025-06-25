FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema necessárias para o mysql-connector-python
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código fonte
COPY . .

# Expõe a porta que o Flask utiliza
EXPOSE 5000

# Define variáveis de ambiente para produção
ENV FLASK_ENV=production

# Valores padrão para as variáveis de ambiente - serão substituídos em produção
ENV DB_USER=root
ENV DB_PASSWORD=root
# Usar RDS_ENDPOINT na EC2/Produção
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=primosfincntrl

# Comando para iniciar a aplicação em produção (0.0.0.0 para permitir acesso externo)
CMD ["python", "app.py"]

# Execução do Entrypoint para subir os dados do Mysql automático.
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
