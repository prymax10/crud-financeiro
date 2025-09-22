#!/bin/bash
set -e

echo "=== PRIMOSFINCNTRL CONTAINER STARTUP ==="
echo "Timestamp: $(date)"

# Função para aguardar o banco de dados estar disponível
wait_for_db() {
    echo "Aguardando banco de dados estar disponível..."
    while ! mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --ssl=0 -e "SELECT 1" >/dev/null 2>&1; do
        echo "Banco de dados não está disponível ainda. Aguardando..."
        sleep 5
    done
    echo "✅ Banco de dados está disponível!"
}

# Função para inicializar o banco de dados
init_database() {
    echo "Inicializando banco de dados..."
    python init_db.py
    echo "✅ Banco de dados inicializado com sucesso!"
}

# Função para verificar se a aplicação está funcionando
health_check() {
    echo "Verificando saúde da aplicação..."
    if curl -f http://localhost:5000/ping >/dev/null 2>&1; then
        echo "✅ Aplicação está funcionando corretamente!"
        return 0
    else
        echo "❌ Aplicação não está respondendo!"
        return 1
    fi
}

# Aguardar banco de dados
echo "🔄 Aguardando banco de dados..."
wait_for_db

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
init_database

# Iniciar a aplicação Flask
echo "🚀 Iniciando aplicação Flask..."
exec python app.py 