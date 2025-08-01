# 🚀 PrimosFinCntrl - Deploy Docker na AWS

Este documento descreve como fazer o deploy da aplicação PrimosFinCntrl usando Docker na infraestrutura AWS.

## 📋 Pré-requisitos

- AWS CLI configurado com SSO
- Terraform instalado
- Acesso à conta AWS com permissões adequadas

## 🏗️ Infraestrutura

A infraestrutura está configurada em `/home/primo/primosfincntrl-infrastructure` e inclui:

- **VPC** com subnets públicas e privadas
- **RDS MySQL** para banco de dados
- **Application Load Balancer** para distribuição de tráfego
- **Auto Scaling Group** com instâncias EC2
- **Security Groups** configurados
- **VPN** para acesso seguro

## 🐳 Modificações Docker

### Dockerfile Otimizado
- Usuário não-root para segurança
- Health checks configurados
- Multi-stage build para otimização
- Python 3.10 para melhor performance

### Entrypoint Melhorado
- Aguarda banco de dados estar disponível
- Inicializa banco automaticamente
- Health checks da aplicação
- Logs estruturados

### Configurações de Produção
- Arquivo `env.production` para variáveis de ambiente
- `docker-compose.yml` otimizado para produção
- Logs rotacionados
- Restart policies configuradas

## 🚀 Deploy Automático

### 1. Deploy Completo
```bash
cd /home/primo/primosfincntrl-infrastructure
./deploy-docker-aws.sh
```

### 2. Deploy Manual por Etapas

#### Aplicar Infraestrutura
```bash
cd /home/primo/primosfincntrl-infrastructure/terraform/environments/sandbox
terraform init
terraform plan
terraform apply
```

#### Verificar Status
```bash
# Verificar instâncias EC2
aws ec2 describe-instances --filters "Name=tag:Project,Values=primosfincntrl"

# Verificar ALB
aws elbv2 describe-load-balancers --names primosfincntrl-sandbox-alb

# Verificar RDS
aws rds describe-db-instances --db-instance-identifier primosfincntrl-sandbox-db
```

## 🔧 Configurações

### Variáveis de Ambiente (env.production)
```bash
# Banco de dados
DB_HOST=primosfincntrl-sandbox-db.cxxxxx.us-east-2.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=PrimosFinCntrl2025x
DB_NAME=primosfincntrl
DB_PORT=3306

# Flask
FLASK_ENV=production
FLASK_APP=app.py
FLASK_DEBUG=false

# Segurança
SECRET_KEY=PrimosFinCntrl2025SecretKeyForProduction
```

### User Data Script
O script `user-data.sh` nas instâncias EC2:
1. Instala Docker
2. Clona o repositório
3. Cria arquivo de configuração
4. Faz build da imagem Docker
5. Executa container com systemd
6. Configura health checks

## 📊 Monitoramento

### Logs
```bash
# Logs do container
docker logs primosfincntrl-app

# Logs do sistema
journalctl -u primosfincntrl-docker

# Logs do user-data
tail -f /var/log/user-data-primosfincntrl.log
```

### Health Checks
- **Container**: Docker health check a cada 30s
- **ALB**: Health check na porta 5000
- **Aplicação**: Endpoint `/ping` para verificação

### Métricas AWS
- CloudWatch para métricas de EC2, RDS e ALB
- Logs centralizados
- Alertas configurados

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Container não inicia
```bash
# Verificar logs
docker logs primosfincntrl-app

# Verificar configuração
cat /opt/primosfincntrl/env.production

# Verificar conectividade com RDS
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "SELECT 1"
```

#### 2. Aplicação não responde
```bash
# Verificar se container está rodando
docker ps

# Verificar porta 5000
netstat -tlnp | grep :5000

# Testar endpoint
curl -f http://localhost:5000/ping
```

#### 3. Problemas de banco de dados
```bash
# Verificar conectividade RDS
aws rds describe-db-instances --db-instance-identifier primosfincntrl-sandbox-db

# Verificar security groups
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx
```

## 🛠️ Manutenção

### Atualizar Aplicação
```bash
# SSH na instância
ssh -i key.pem ec2-user@instance-ip

# Parar container
sudo systemctl stop primosfincntrl-docker

# Pull código atualizado
cd /opt/primosfincntrl
git pull

# Rebuild e restart
sudo systemctl start primosfincntrl-docker
```

### Backup do Banco
```bash
# Backup automático configurado no RDS
# Backup manual se necessário
aws rds create-db-snapshot \
    --db-instance-identifier primosfincntrl-sandbox-db \
    --db-snapshot-identifier backup-manual-$(date +%Y%m%d)
```

## 📈 Escalabilidade

- **Auto Scaling**: 2-6 instâncias baseado em CPU
- **Load Balancer**: Distribuição de tráfego
- **RDS**: Multi-AZ para alta disponibilidade
- **Backup**: Automático com retenção configurada

## 🔒 Segurança

- **Container**: Usuário não-root
- **Network**: Security groups restritivos
- **Database**: RDS com encryption
- **VPN**: Acesso seguro às instâncias
- **IAM**: Permissões mínimas necessárias

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs do sistema
2. Consultar métricas CloudWatch
3. Verificar status dos serviços AWS
4. Revisar configurações de rede e segurança 