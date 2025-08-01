#!/bin/bash

# Script para deploy da aplicação PrimosFinCntrl na AWS
# Este script será executado nas instâncias EC2

set -e

echo "🚀 Deployando PrimosFinCntrl na AWS..."

# Configurações
APP_DIR="/opt/primosfincntrl"
APP_USER="primosfincntrl"
REPO_URL="https://github.com/prymax10/crud-financeiro.git"

# Criar usuário se não existir
if ! id "$APP_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$APP_DIR" "$APP_USER"
fi

# Criar diretório da aplicação
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Clonar repositório
if [ ! -d ".git" ]; then
    git clone "$REPO_URL" .
else
    git pull origin main
fi

# Instalar dependências Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variáveis de ambiente
cat > .env << 'ENV_EOF'
# Configurações de banco de dados para produção RDS
DB_USER=admin
DB_PASSWORD=PrimosFinCntrl2025x
DB_HOST=primosfincntrl-sandbox-db.cxxxxx.us-east-2.rds.amazonaws.com
DB_PORT=3306
DB_NAME=primosfincntrl

# Configuração Flask para produção
FLASK_ENV=production
FLASK_APP=app.py
ENV_EOF

# Configurar permissões
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
chmod 600 .env

# Criar serviço systemd
cat > /etc/systemd/system/primosfincntrl.service << 'SERVICE_EOF'
[Unit]
Description=PrimosFinCntrl Financial Control Application
After=network.target

[Service]
Type=simple
User=primosfincntrl
Group=primosfincntrl
WorkingDirectory=/opt/primosfincntrl
Environment=FLASK_APP=app.py
Environment=FLASK_ENV=production
EnvironmentFile=/opt/primosfincntrl/.env
ExecStartPre=/opt/primosfincntrl/venv/bin/python /opt/primosfincntrl/init_db.py
ExecStart=/opt/primosfincntrl/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Recarregar systemd e habilitar serviço
systemctl daemon-reload
systemctl enable primosfincntrl
systemctl start primosfincntrl

echo "✅ Deploy concluído!"
echo "📊 Status do serviço:"
systemctl status primosfincntrl --no-pager

echo "🌐 Testando aplicação..."
sleep 10
curl -f http://localhost:5000/ping || echo "❌ Aplicação não respondeu"
