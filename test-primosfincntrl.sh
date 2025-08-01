#!/bin/bash

# Script para testar a aplicação PrimosFinCntrl

echo "🧪 TESTANDO APLICAÇÃO PRIMOSFINCNTRL"
echo "===================================="

# Testar aplicação local
echo "1. Testando aplicação local..."
cd /home/primo/primosfincntrl

# Verificar se Flask está instalado
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask não instalado"
    exit 1
fi

# Testar se a aplicação inicia
echo "2. Testando inicialização da aplicação..."
timeout 30s python3 app.py &
APP_PID=$!
sleep 5

# Testar endpoints
echo "3. Testando endpoints..."
curl -f http://localhost:5000/ping && echo "✅ /ping OK"
curl -f http://localhost:5000/ && echo "✅ / OK"
curl -f http://localhost:5000/health && echo "✅ /health OK"

# Parar aplicação
kill $APP_PID 2>/dev/null || true

echo "✅ Testes concluídos!"
