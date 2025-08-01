#!/bin/bash

# Script para configurar o banco de dados RDS

echo "🗄️ CONFIGURANDO BANCO DE DADOS RDS"
echo "==================================="

# Configurações do RDS (serão substituídas pelo Terraform)
DB_HOST="primosfincntrl-sandbox-db.cxxxxx.us-east-2.rds.amazonaws.com"
DB_USER="admin"
DB_PASSWORD="PrimosFinCntrl2025x"
DB_NAME="primosfincntrl"

echo "📊 Configurações do banco:"
echo "Host: $DB_HOST"
echo "User: $DB_USER"
echo "Database: $DB_NAME"

# Testar conexão
echo "🔍 Testando conexão com o banco..."
if command -v mysql &> /dev/null; then
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" && echo "✅ Conexão OK"
else
    echo "⚠️ MySQL client não encontrado"
fi

# Executar inicialização do banco
echo "🚀 Inicializando banco de dados..."
cd /home/primo/primosfincntrl
python3 init_db.py

echo "✅ Configuração do banco concluída!"
