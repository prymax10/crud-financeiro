
# CRUD Financeiro na AWS (Manual Setup via Console)

Este projeto consiste em uma aplicação web (backend + frontend) para controle financeiro, implantada manualmente na AWS, conforme escopo de onboarding DevOps/SRE.

---

## 📌 Escopo Atendido

- ✅ Infraestrutura criada manualmente via Console AWS
- ✅ Deploy do backend (Flask) e frontend (HTML/JS) com Docker em EC2
- ✅ Banco de dados MySQL no RDS
- ✅ ALB (Load Balancer) com Health Checks
- ✅ Alta disponibilidade com EC2 principal e reserva
- ✅ Testes realizados com sucesso

---

## 🧩 Estrutura da Infra

### VPC

- CIDR: `10.0.0.0/16`
- Subnets:
  - `subnet-public-a` (us-east-2a): `10.0.10.0/24`
  - `subnet-public-b` (us-east-2b): `10.0.20.0/24`
  - `subnet-private-a` (us-east-2a): `10.0.30.0/24`
  - `subnet-private-b` (us-east-2b): `10.0.40.0/24`

### Gateways

- Internet Gateway: Conectado à VPC
- NAT Gateway: Implantado em `subnet-public-a`, associado a um EIP

### Route Tables

- Rota pública: `0.0.0.0/0` -> IGW
- Rota privada: `0.0.0.0/0` -> NAT Gateway

---

## 💻 EC2

### Instâncias

- **EC2-A (principal)**
  - Nome: `crud-finance-ec2-a`
  - IP Público: `18.216.31.131`
  - Zona: `us-east-2a`
  - Rodando containers do backend e frontend
- **EC2-B (reserva)**
  - Nome: `crud-finance-ec2-b`
  - IP Público: `3.23.102.54`
  - Zona: `us-east-2b`
  - Configuração idêntica à EC2-A (docker-compose com .env)

### Docker

- Docker instalado via script manual
- Backend e frontend empacotados em um container
- `docker-compose.yml` usa `.env` com as variáveis do RDS

---

## 🐬 RDS (MySQL)

- Nome: `crud-finance-db-v2`
- Endpoint: `crud-finance-db-v2.couyq2fi02mr.us-east-2.rds.amazonaws.com`
- Porta: `3306`
- Público: `false` (acesso apenas via EC2)
- Banco: `crud_financeiro`
- Usuário: `admin`
- Senha: `Devopscrud25` (armazenada no `.env`)

---

## ⚖️ Load Balancer

- ALB: `crud-finance-alb-233355946.us-east-2.elb.amazonaws.com`
- Listener: Porta 80 -> Target Group
- Target Group: EC2-A e EC2-B
  - Health Check: `/ping`
  - Intervalo: 5s
  - Timeout: 2s
  - Healthy threshold: 2

---

## 🔐 Security Groups

- **EC2 / ALB:**
  - Inbound: 80 (HTTP) de `0.0.0.0/0`
  - Inbound: 22 (SSH) de IP pessoal
- **RDS:**
  - Inbound: 3306 apenas das EC2 (via SG)

---

## 🚀 Deploy e Repositório

- Repositório GitHub: [crud-financeiro](https://github.com/prymax10/crud-financeiro)
- EC2-A fez push do código
- EC2-B fez `git clone` e usou `.env` com mesmo RDS

---

## ✅ Testes Realizados

- `/ping`: 200 OK via ALB
- `/api/categorias`: carregou com sucesso
- `/api/despesas`: integração com RDS
- Toda interface web funcionando
- ALB alternando entre instâncias (testado parando EC2-A, pós EC2-B.)
- Erros 500 diagnosticados e resolvidos

---

## 🧠 Observações

- `init_db.sql` utilizado para inicialização do banco
- `init_db.py` foi ajustado para não recriar o banco, apenas as tabelas
- `.env` com as credenciais precisa ser criado nas duas EC2
