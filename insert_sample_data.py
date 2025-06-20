#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para inserir dados de exemplo no banco de dados SQLite
"""

import sqlite3
import os
from datetime import datetime, timedelta

# Caminho para o banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'primosfincntrl.db')

def insert_sample_data():
    """
    Insere dados de exemplo no banco de dados
    """
    # Verifica se o banco existe
    if not os.path.exists(DB_PATH):
        print(f"Banco de dados não encontrado em: {DB_PATH}")
        return False
    
    # Conecta ao banco de dados
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Limpa dados existentes
        cursor.execute("DELETE FROM despesas")
        cursor.execute("DELETE FROM categorias")
        
        # Insere categorias
        categorias = [
            (1, 'Alimentação', '#FF5733'),
            (2, 'Transporte', '#33A8FF'),
            (3, 'Moradia', '#33FF57'),
            (4, 'Lazer', '#F033FF'),
            (5, 'Saúde', '#FF3333'),
            (6, 'Educação', '#33FFF0')
        ]
        
        cursor.executemany(
            "INSERT INTO categorias (id, nome, cor) VALUES (?, ?, ?)",
            categorias
        )
        
        # Gera datas para os últimos 30 dias
        hoje = datetime.now().date()
        datas = [(hoje - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
        
        # Insere despesas de exemplo
        despesas = [
            ('Supermercado', -150.75, datas[0], 1),
            ('Restaurante', -45.90, datas[1], 1),
            ('Uber', -22.50, datas[2], 2),
            ('Combustível', -200.00, datas[3], 2),
            ('Aluguel', -1200.00, datas[4], 3),
            ('Conta de luz', -120.50, datas[5], 3),
            ('Cinema', -35.00, datas[6], 4),
            ('Consulta médica', -150.00, datas[7], 5),
            ('Curso online', -89.90, datas[8], 6),
            ('Padaria', -15.75, datas[9], 1),
            ('Farmácia', -65.30, datas[10], 5),
            ('Internet', -99.90, datas[11], 3),
            ('Estacionamento', -12.00, datas[12], 2),
            ('Livros', -78.50, datas[13], 6),
            ('Lanche', -18.90, datas[14], 1)
        ]
        
        cursor.executemany(
            "INSERT INTO despesas (descricao, valor, data, categoria_id) VALUES (?, ?, ?, ?)",
            despesas
        )
        
        # Confirma as alterações
        conn.commit()
        print(f"Dados de exemplo inseridos com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao inserir dados de exemplo: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_sample_data()
