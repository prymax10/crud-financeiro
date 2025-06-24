# Instruções para Deployment na AWS EC2 com RDS

Este documento contém instruções detalhadas para implantar a aplicação Primo'sFinCntrl em um ambiente AWS usando EC2 para hospedar a aplicação e RDS MySQL para o banco de dados.

## Pré-requisitos

1. Uma instância EC2 em execução com Docker e Docker Compose instalados
2. Uma instância RDS MySQL configurada e acessível pela EC2
3. Credenciais de acesso ao RDS MySQL

## Passos para Deployment

### 1. Clonar o repositório na instância EC2

```bash
git clone https://github.com/prymax10/crud-financeiro.git
cd crud-financeiro
```

### 2. Configurar variáveis de ambiente para o RDS

Crie um arquivo `.env` na raiz do projeto:

```bash
cat > .env << EOL
# Configurações do RDS
DB_USER=seu_usuario_rds
DB_PASSWORD=sua_senha_rds
DB_HOST=seu-endpoint-rds.region.rds.amazonaws.com
DB_PORT=3306
DB_NAME=primosfincntrl
EOL
```

### 3. Construir e iniciar a aplicação com Docker Compose

```bash
docker-compose build
docker-compose up -d
```

### 4. Verificar se a aplicação está em execução

```bash
docker-compose ps
docker-compose logs
```

A aplicação estará disponível em: http://seu-ip-ec2:5000

### 5. Configuração do Load Balancer (Opcional, se você estiver usando ALB)

Se você estiver usando um Application Load Balancer da AWS:

1. Configure seu grupo alvo para apontar para a porta 5000 da instância EC2
2. Certifique-se de que o Load Balancer está encaminhando o tráfego HTTP na porta 80 para a porta 5000 da EC2
3. O frontend está configurado para usar automaticamente o DNS do ALB: 
   `crud-finance-alb-233355946.us-east-2.elb.amazonaws.com`

## Manutenção

### Atualização da aplicação

Para atualizar a aplicação com novas alterações do repositório:

```bash
cd /caminho/para/crud-financeiro
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Visualizar logs da aplicação

```bash
docker-compose logs -f
```

### Conectar-se ao banco de dados RDS para inspeção manual

```bash
mysql -u seu_usuario_rds -p -h seu-endpoint-rds.region.rds.amazonaws.com primosfincntrl
```

## Solução de Problemas

1. **Erro de conexão com o RDS**: Verifique se o grupo de segurança do RDS permite conexões da instância EC2
2. **Frontend não pode acessar a API**: Verifique as configurações CORS e se a URL base da API está correta
3. **Tabelas não criadas no RDS**: Conecte-se manualmente ao RDS e execute o script `init_db.py`
