# Primo'sFinCntrl - Sistema de Controle Financeiro

Sistema de controle financeiro pessoal para gerenciamento de despesas, com visualização de estatísticas e categorização de gastos. Esta versão do sistema está migrada para utilizar MySQL com SQLAlchemy, pronta para deployment na AWS.

## Estrutura do Projeto

```
primosfincntrl/
│── app/
│   │── models/
│   │   │── database.py   # Configuração do MySQL com SQLAlchemy
│   │   │── despesa.py    # Modelo de despesas
│   │   │── categoria.py  # Modelo de categorias
│   │   └── estatistica.py # Modelo para estatísticas
│   │── routes/         # Rotas da API
│   │   │── despesas_routes.py
│   │   │── categorias_routes.py
│   │   └── estatisticas_routes.py
│   └── services/
│── static/           # Frontend
│   │── css/
│   │   └── style.css
│   │── js/
│   │   │── api.js
│   │   │── api-url-config.js # Configuração da URL da API
│   │   │── ui.js
│   │   └── app.js
│   └── img/
│── templates/
│   └── index.html
│── app.py            # Arquivo principal da aplicação
│── init_db.py        # Script para inicialização do banco
│── requirements.txt   # Dependências Python
│── Dockerfile         # Build da imagem Docker
│── docker-compose.yml        # Composição para desenvolvimento
└── docker-compose.prod.yml   # Composição para produção com RDS
```

## Requisitos

- Python 3.8+
- MySQL 8.0+
- Docker e Docker Compose (para implantação)
- Navegador web moderno

## Instalação e Execução Local

1. Clone o repositório:
```bash
git clone https://github.com/prymax10/crud-financeiro.git
cd primosfincntrl
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados MySQL:
```sql
CREATE DATABASE primosfincntrl;
```

4. Ajuste as configurações de conexão no arquivo `app.py`:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'primosfincntrl'
```

## Execução

1. Inicie o servidor Flask:
```
python app.py
```

2. Acesse a aplicação no navegador:
```
http://localhost:5000
```

## Funcionalidades

- Cadastro, edição e exclusão de despesas
- Categorização de despesas
- Filtros por período (Hoje, Semana, Mês, Ano, Todos)
- Visualização de estatísticas com gráficos
- Resumo de gastos por categoria

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS e JavaScript puro
- **Banco de Dados**: MySQL
- **Bibliotecas**: Bootstrap 5, Chart.js

## Estrutura do Banco de Dados

### Tabela: categorias
- id (INT, PK)
- nome (VARCHAR)
- cor (VARCHAR)

### Tabela: despesas
- id (INT, PK)
- descricao (VARCHAR)
- valor (DECIMAL)
- data (DATE)
- categoria_id (INT, FK)
