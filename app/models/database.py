#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de configuração e conexão com o banco de dados MySQL usando SQLAlchemy
"""

import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

# Definição dos modelos SQLAlchemy
class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(20), nullable=False)
    
    # Relação com despesas
    despesas = db.relationship('Despesa', backref='categoria', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cor': self.cor
        }

class Despesa(db.Model):
    __tablename__ = 'despesas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': self.valor,
            'data': self.data.strftime('%Y-%m-%d'),
            'categoria_id': self.categoria_id,
            'categoria_nome': self.categoria.nome if self.categoria else None,
            'categoria_cor': self.categoria.cor if self.categoria else None
        }

def init_db(app):
    """
    Inicializa o banco de dados MySQL usando SQLAlchemy
    """
    try:
        # Configuração do banco de dados a partir de variáveis de ambiente
        # Quando não fornecidas, usa valores padrão para desenvolvimento local
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', 'root')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_name = os.getenv('DB_NAME', 'primosfincntrl')
        
        # Configura a URI do MySQL
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Inicializa a aplicação com SQLAlchemy
        db.init_app(app)
        
        # Cria as tabelas e adiciona categorias padrão
        with app.app_context():
            db.create_all()
            logger.info("Banco de dados MySQL inicializado com sucesso")
            criar_categorias_padrao()
            
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {e}")
        raise

def criar_categorias_padrao():
    """
    Insere categorias padrão se a tabela estiver vazia
    """
    try:
        # Verifica se já existem categorias
        if Categoria.query.count() == 0:
            categorias_padrao = [
                Categoria(nome='Alimentação', cor='#FF5733'),
                Categoria(nome='Transporte', cor='#33FF57'),
                Categoria(nome='Moradia', cor='#3357FF'),
                Categoria(nome='Saúde', cor='#FF33A8'),
                Categoria(nome='Educação', cor='#33A8FF'),
                Categoria(nome='Lazer', cor='#A833FF'),
                Categoria(nome='Vestuário', cor='#FFD700'),
                Categoria(nome='Outros', cor='#808080')
            ]
            
            # Adiciona todas as categorias
            db.session.add_all(categorias_padrao)
            db.session.commit()
            logger.info("Categorias padrão criadas com sucesso")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar categorias padrão: {e}")
        raise
