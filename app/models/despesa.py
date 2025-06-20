#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para manipulação de despesas no banco de dados
"""

import sqlite3
from datetime import datetime
from app.models.database import get_db

class Despesa:
    """
    Classe para manipulação de despesas no banco de dados
    """
    
    @staticmethod
    def listar(periodo=None):
        """
        Lista todas as despesas do banco de dados
        
        Args:
            periodo (str, optional): Filtro de período (diario, semanal, mensal, anual)
        
        Returns:
            list: Lista de despesas
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query base
        query = """
        SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id,
               c.nome as categoria_nome, c.cor as categoria_cor
        FROM despesas d
        LEFT JOIN categorias c ON d.categoria_id = c.id
        """
        
        # Adiciona filtro de período se necessário
        params = []
        if periodo:
            hoje = datetime.now().date()
            
            hoje_str = hoje.strftime('%Y-%m-%d')
            if periodo == 'diario':
                query += " WHERE date(d.data) = ?"
                params.append(hoje_str)
            elif periodo == 'semanal':
                # Considera a semana atual (últimos 7 dias)
                query += " WHERE date(d.data) >= date(?, '-7 days')"
                params.append(hoje_str)
            elif periodo == 'mensal':
                # Considera o mês atual
                query += " WHERE strftime('%Y-%m', d.data) = strftime('%Y-%m', ?)"
                params.append(hoje_str)
            elif periodo == 'anual':
                # Considera o ano atual
                query += " WHERE strftime('%Y', d.data) = strftime('%Y', ?)"
                params.append(hoje_str)
        
        # Ordena por data mais recente
        query += " ORDER BY d.data DESC"
        
        cursor.execute(query, params)
        despesas = cursor.fetchall()
        
        # Converte o resultado para lista de dicionários e formata as datas
        result = []
        for row in despesas:
            despesa = dict(row)
            # Formata a data para o formato brasileiro
            data = datetime.strptime(despesa['data'], '%Y-%m-%d')
            despesa['data'] = data.strftime('%d/%m/%Y')
            result.append(despesa)
        
        cursor.close()
        return result
    
    @staticmethod
    def obter_por_id(despesa_id):
        """
        Obtém uma despesa pelo ID
        
        Args:
            despesa_id (int): ID da despesa
        
        Returns:
            dict: Dados da despesa ou None se não encontrada
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
        SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id,
               c.nome as categoria_nome, c.cor as categoria_cor
        FROM despesas d
        LEFT JOIN categorias c ON d.categoria_id = c.id
        WHERE d.id = ?
        """
        
        cursor.execute(query, (despesa_id,))
        row = cursor.fetchone()
        
        despesa = None
        if row:
            despesa = dict(row)
            # A data já está no formato correto para edição em SQLite
        
        cursor.close()
        return despesa
    
    @staticmethod
    def criar(dados):
        """
        Cria uma nova despesa no banco de dados
        
        Args:
            dados (dict): Dados da despesa (descricao, valor, data, categoria_id)
        
        Returns:
            int: ID da despesa criada
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # Garante que o valor seja negativo (despesa)
        valor = float(dados['valor'])
        if valor > 0:
            valor = -valor
        
        query = """
        INSERT INTO despesas (descricao, valor, data, categoria_id)
        VALUES (?, ?, ?, ?)
        """
        
        cursor.execute(
            query,
            (
                dados['descricao'],
                valor,
                dados['data'],
                dados['categoria_id']
            )
        )
        
        despesa_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return despesa_id
    
    @staticmethod
    def atualizar(despesa_id, dados):
        """
        Atualiza uma despesa existente
        
        Args:
            despesa_id (int): ID da despesa
            dados (dict): Novos dados da despesa
        
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # Garante que o valor seja negativo (despesa)
        valor = float(dados['valor'])
        if valor > 0:
            valor = -valor
        
        query = """
        UPDATE despesas
        SET descricao = ?, valor = ?, data = ?, categoria_id = ?
        WHERE id = ?
        """
        
        cursor.execute(
            query,
            (
                dados['descricao'],
                valor,
                dados['data'],
                dados['categoria_id'],
                despesa_id
            )
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        
        return success
    
    @staticmethod
    def excluir(despesa_id):
        """
        Exclui uma despesa do banco de dados
        
        Args:
            despesa_id (int): ID da despesa
        
        Returns:
            bool: True se excluída com sucesso, False caso contrário
        """
        conn = get_db()
        cursor = conn.cursor()
        
        query = "DELETE FROM despesas WHERE id = ?"
        cursor.execute(query, (despesa_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        
        return success
