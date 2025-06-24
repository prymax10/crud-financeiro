#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para manipulação de categorias no banco de dados usando SQLAlchemy
"""

from app.models.database import db, Categoria as CategoriaModel

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
        categorias = CategoriaModel.query.order_by(CategoriaModel.nome).all()
        return [categoria.to_dict() for categoria in categorias]
    
    @staticmethod
    def obter_por_id(categoria_id):
        """
        Obtém uma categoria pelo ID
        
        Args:
            categoria_id (int): ID da categoria
        
        Returns:
            dict: Dados da categoria ou None se não encontrada
        """
        categoria = CategoriaModel.query.get(categoria_id)
        return categoria.to_dict() if categoria else None
    
    @staticmethod
    def criar_categorias_padrao():
        """
        Insere categorias padrão se a tabela estiver vazia
        
        Returns:
            bool: True se as categorias foram criadas, False caso contrário
        """
        try:
            # Verifica se já existem categorias
            if CategoriaModel.query.count() > 0:
                return False
            
            categorias_padrao = [
                CategoriaModel(nome='Alimentação', cor='#FF5733'),
                CategoriaModel(nome='Transporte', cor='#33FF57'),
                CategoriaModel(nome='Moradia', cor='#3357FF'),
                CategoriaModel(nome='Saúde', cor='#FF33A8'),
                CategoriaModel(nome='Educação', cor='#33A8FF'),
                CategoriaModel(nome='Lazer', cor='#A833FF'),
                CategoriaModel(nome='Vestuário', cor='#FFD700'),
                CategoriaModel(nome='Outros', cor='#808080')
            ]
            
            db.session.add_all(categorias_padrao)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar categorias padrão: {e}")
            return False
