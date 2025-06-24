#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de inicialização do banco de dados
Pode ser executado separadamente para criar as tabelas e inserir dados iniciais
"""

import os
from flask import Flask
from app.models.database import db, init_db, criar_categorias_padrao
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def init_database():
    """
    Inicializa o banco de dados, criando tabelas e categorias padrão
    """
    # Cria uma instância da aplicação Flask
    app = Flask(__name__)
    
    # Configura a aplicação com SQLAlchemy
    init_db(app)
    
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos
        db.create_all()
        print("Tabelas criadas com sucesso!")
        
        # Cria categorias padrão
        criar_categorias_padrao()
        print("Categorias padrão inseridas com sucesso!")
        
        print("Inicialização do banco de dados concluída!")

if __name__ == "__main__":
    init_database()
