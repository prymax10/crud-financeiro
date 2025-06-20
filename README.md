# Primo'sFinCntrl - Sistema de Controle Financeiro

Sistema de controle financeiro pessoal para gerenciamento de despesas, com visualização de estatísticas e categorização de gastos.

## Estrutura do Projeto

```
primosfincntrl/
├── app/
│   ├── models/
│   │   ├── database.py
│   │   ├── despesa.py
│   │   ├── categoria.py
│   │   └── estatistica.py
│   ├── routes/
│   │   ├── despesas_routes.py
│   │   ├── categorias_routes.py
│   │   └── estatisticas_routes.py
│   └── services/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js
│   │   ├── ui.js
│   │   └── app.js
│   └── img/
├── templates/
│   └── index.html
├── app.py
└── requirements.txt
```

## Requisitos

- Python 3.8+
- MySQL 5.7+
- Navegador web moderno

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/primosfincntrl.git
cd primosfincntrl
```

2. Instale as dependências:
```
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
