#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de inicialização do banco de dados
Cria tabelas e insere dados iniciais automaticamente
"""

import os
import mysql.connector
from flask import Flask
from app.models.database import db, init_db
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def criar_banco_se_nao_existir():
    """
    Conecta ao MySQL e cria o banco se não existir
    """
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    cursor = conexao.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conexao.close()
    print(f"✅ Banco '{db_name}' verificado/criado com sucesso.")

def init_database():
    """
    Inicializa o banco de dados, criando tabelas e categorias padrão
    """
    criar_banco_se_nao_existir()

    # Cria uma instância da aplicação Flask
    app = Flask(__name__)
    
    # Configura a aplicação com SQLAlchemy
    init_db(app)
    
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Cria categorias padrão manualmente
        from app.models.database import Categoria
        
        categorias = [
            {"nome": "Alimentação", "cor": "#FF5733"},
            {"nome": "Transporte", "cor": "#33FF57"},
            {"nome": "Moradia", "cor": "#3357FF"},
            {"nome": "Saúde", "cor": "#FF33A8"},
            {"nome": "Educação", "cor": "#33A8FF"},
            {"nome": "Lazer", "cor": "#A833FF"},
            {"nome": "Vestuário", "cor": "#FFD700"},
            {"nome": "Outros", "cor": "#808080"}
        ]
        
        categorias_adicionadas = 0
        for cat in categorias:
            # Verifica se cada categoria existe individualmente
            categoria_existente = Categoria.query.filter_by(nome=cat["nome"]).first()
            if not categoria_existente:
                nova_categoria = Categoria(nome=cat["nome"], cor=cat["cor"])
                db.session.add(nova_categoria)
                categorias_adicionadas += 1
        
        if categorias_adicionadas > 0:
            db.session.commit()
            print(f"✅ {categorias_adicionadas} categorias adicionadas com sucesso!")
        else:
            print("ℹ️ Todas as categorias já existem no banco de dados.")
        
        print("✅ Inicialização do banco de dados concluída!")

if __name__ == "__main__":
    init_database()

