#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de configuração e conexão com o banco de dados SQLite
"""

import sqlite3
import os
from flask import g

# Caminho para o arquivo do banco de dados SQLite
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'primosfincntrl.db')

def init_db(app):
    """
    Inicializa o banco de dados SQLite
    """
    # Registra a função de fechamento da conexão
    app.teardown_appcontext(close_db)
    
    try:
        # Verifica se o banco já existe
        db_exists = os.path.exists(DATABASE_PATH)
        
        # Se o banco não existia, inicializa o esquema com o contexto da aplicação
        if not db_exists:
            with app.app_context():
                init_schema()
                print(f"Banco de dados criado em: {DATABASE_PATH}")
        else:
            print(f"Usando banco de dados existente em: {DATABASE_PATH}")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

def get_db():
    """
    Retorna uma conexão com o banco de dados
    Se já existe uma conexão na requisição atual, reutiliza
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        # Configura para retornar rows como dicts
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Fecha a conexão com o banco de dados ao final da requisição
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_schema():
    """
    Inicializa o esquema do banco de dados, criando as tabelas necessárias
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Criação da tabela de categorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cor TEXT NOT NULL
    )
    ''')
    
    # Criação da tabela de despesas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    ''')
    
    # Inserção de categorias padrão
    cursor.execute('SELECT COUNT(*) FROM categorias')
    count = cursor.fetchone()[0]
    
    if count == 0:
        categorias_padrao = [
            ('Alimentação', '#FF5733'),
            ('Transporte', '#33FF57'),
            ('Moradia', '#3357FF'),
            ('Saúde', '#FF33A8'),
            ('Educação', '#33A8FF'),
            ('Lazer', '#A833FF'),
            ('Vestuário', '#FFD700'),
            ('Outros', '#808080')
        ]
        
        cursor.executemany(
            'INSERT INTO categorias (nome, cor) VALUES (?, ?)',
            categorias_padrao
        )
    
    conn.commit()
