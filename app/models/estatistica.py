#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para geração de estatísticas a partir das despesas
"""

import sqlite3
from app.models.database import get_db
from datetime import datetime

class Estatistica:
    """
    Classe para geração de estatísticas a partir das despesas
    """
    
    @staticmethod
    def total_despesas(periodo=None):
        """
        Calcula o total de despesas para um determinado período
        
        Args:
            periodo (str, optional): Filtro de período (diario, semanal, mensal, anual)
        
        Returns:
            float: Total de despesas
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query base
        query = "SELECT SUM(valor) FROM despesas"
        
        # Adiciona filtro de período se necessário
        params = []
        if periodo:
            hoje = datetime.now().date()
            
            hoje_str = hoje.strftime('%Y-%m-%d')
            if periodo == 'diario':
                query += " WHERE date(data) = ?"
                params.append(hoje_str)
            elif periodo == 'semanal':
                # Considera a semana atual (últimos 7 dias)
                query += " WHERE date(data) >= date(?, '-7 days')"
                params.append(hoje_str)
            elif periodo == 'mensal':
                # Considera o mês atual
                query += " WHERE strftime('%Y-%m', data) = strftime('%Y-%m', ?)"
                params.append(hoje_str)
            elif periodo == 'anual':
                # Considera o ano atual
                query += " WHERE strftime('%Y', data) = strftime('%Y', ?)"
                params.append(hoje_str)
        
        cursor.execute(query, params)
        total = cursor.fetchone()[0]
        cursor.close()
        
        # Se não houver despesas, retorna 0
        return float(total) if total else 0.0
    
    @staticmethod
    def despesas_por_categoria(periodo=None):
        """
        Calcula o total de despesas agrupadas por categoria
        
        Args:
            periodo (str, optional): Filtro de período (diario, semanal, mensal, anual)
        
        Returns:
            list: Lista de despesas por categoria
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query base
        query = """
        SELECT c.id, c.nome, c.cor, SUM(d.valor) as total
        FROM despesas d
        JOIN categorias c ON d.categoria_id = c.id
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
        
        # Agrupa por categoria e ordena pelo total (maior para menor)
        query += " GROUP BY c.id, c.nome, c.cor ORDER BY total ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Converte para lista de dicionários
        categorias = [dict(row) for row in rows]
        
        # Calcula o total geral para percentuais
        total_geral = sum(abs(float(cat['total'])) for cat in categorias)
        
        # Adiciona o percentual para cada categoria
        for cat in categorias:
            cat['percentual'] = round(abs(float(cat['total'])) / total_geral * 100, 2) if total_geral > 0 else 0
            cat['total'] = abs(float(cat['total']))  # Converte para positivo para exibição e serialização JSON
        
        return categorias
