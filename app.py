#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arquivo principal da aplicação Primo'sFinCntrl
Responsável por inicializar o servidor Flask e registrar as rotas
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from app.routes import despesas_routes, categorias_routes, estatisticas_routes
from app.models.database import init_db
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Inicializa o banco de dados MySQL
# A configuração de SQLAlchemy será feita dentro da função init_db
try:
    init_db(app)
    print("Banco de dados MySQL inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o banco de dados: {e}")
    raise

# Registra as rotas da aplicação
app.register_blueprint(despesas_routes.bp, url_prefix='/api/despesas')
app.register_blueprint(categorias_routes.bp, url_prefix='/api/categorias')
app.register_blueprint(estatisticas_routes.bp, url_prefix='/api/estatisticas')

# Rota principal que serve o template HTML
@app.route('/')
def index():
    """Endpoint principal que serve a página HTML"""
    return render_template('index.html')

# Rota de verificação de saúde da API
@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({"message": "pong"})

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500

# Execução da aplicação
if __name__ == '__main__':
    # Em produção, listen em todas as interfaces e desliga o modo debug
    is_production = os.environ.get('FLASK_ENV') == 'production'
    host = '0.0.0.0' if is_production else '127.0.0.1'
    debug = not is_production
    
    app.run(host=host, debug=debug, port=5000)
