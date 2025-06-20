#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para manipulação de categorias no banco de dados
"""

import sqlite3
from app.models.database import get_db

class Categoria:
    """
    Classe para manipulação de categorias no banco de dados
    """
    
    @staticmethod
    def listar():
        """
        Lista todas as categorias do banco de dados
        
        Returns:
            list: Lista de categorias
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT id, nome, cor FROM categorias ORDER BY nome"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        categorias = [dict(row) for row in rows]
        cursor.close()
        
        return categorias
    
    @staticmethod
    def obter_por_id(categoria_id):
        """
        Obtém uma categoria pelo ID
        
        Args:
            categoria_id (int): ID da categoria
        
        Returns:
            dict: Dados da categoria ou None se não encontrada
        """
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT id, nome, cor FROM categorias WHERE id = ?"
        cursor.execute(query, (categoria_id,))
        
        row = cursor.fetchone()
        categoria = dict(row) if row else None
        cursor.close()
        
        return categoria
