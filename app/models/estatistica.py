#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para geração de estatísticas a partir das despesas usando SQLAlchemy
"""

from app.models.database import db, Despesa as DespesaModel, Categoria as CategoriaModel
from datetime import datetime, timedelta
import sqlalchemy as sa

class Estatistica:
    """
    Classe para geração de estatísticas a partir das despesas usando SQLAlchemy
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
        # Query base
        query = db.session.query(sa.func.sum(DespesaModel.valor))
        
        # Adiciona filtro de período se necessário
        hoje = datetime.now().date()
        
        if periodo:
            if periodo == 'diario':
                # Despesas do dia atual
                query = query.filter(sa.func.date(DespesaModel.data) == hoje)
            elif periodo == 'semanal':
                # Despesas da última semana (7 dias)
                data_inicio = hoje - timedelta(days=7)
                query = query.filter(DespesaModel.data >= data_inicio)
            elif periodo == 'mensal':
                # Despesas do mês atual
                inicio_mes = datetime(hoje.year, hoje.month, 1).date()
                query = query.filter(DespesaModel.data >= inicio_mes)
            elif periodo == 'anual':
                # Despesas do ano atual
                inicio_ano = datetime(hoje.year, 1, 1).date()
                query = query.filter(DespesaModel.data >= inicio_ano)
        
        total = query.scalar()
        
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
        # Query base para selecionar id, nome, cor da categoria e o total de despesas
        query = db.session.query(
            CategoriaModel.id,
            CategoriaModel.nome,
            CategoriaModel.cor,
            sa.func.sum(DespesaModel.valor).label('total')
        ).join(DespesaModel, CategoriaModel.id == DespesaModel.categoria_id)
        
        # Adiciona filtro de período se necessário
        hoje = datetime.now().date()
        
        if periodo:
            if periodo == 'diario':
                # Despesas do dia atual
                query = query.filter(sa.func.date(DespesaModel.data) == hoje)
            elif periodo == 'semanal':
                # Despesas da última semana (7 dias)
                data_inicio = hoje - timedelta(days=7)
                query = query.filter(DespesaModel.data >= data_inicio)
            elif periodo == 'mensal':
                # Considera o mês atual
                inicio_mes = datetime(hoje.year, hoje.month, 1).date()
                query = query.filter(DespesaModel.data >= inicio_mes)
            elif periodo == 'anual':
                # Considera o ano atual
                inicio_ano = datetime(hoje.year, 1, 1).date()
                query = query.filter(DespesaModel.data >= inicio_ano)
        
        # Agrupa por categoria e ordena pelo valor absoluto das despesas (decrescente)
        query = query.group_by(CategoriaModel.id, CategoriaModel.nome, CategoriaModel.cor)
        query = query.order_by(sa.desc(sa.func.abs(sa.func.sum(DespesaModel.valor))))
        
        results = query.all()
        
        # Formata o resultado
        categorias_despesas = []
        for result in results:
            categorias_despesas.append({
                'id': result.id,
                'nome': result.nome,
                'cor': result.cor,
                'total': float(result.total) if result.total else 0.0
            })
        
        # Calcula o total geral para percentuais
        total_geral = sum(abs(float(cat['total'])) for cat in categorias_despesas)
        
        # Adiciona o percentual para cada categoria
        for cat in categorias_despesas:
            cat['percentual'] = round(abs(float(cat['total'])) / total_geral * 100, 2) if total_geral > 0 else 0
            cat['total'] = abs(float(cat['total']))  # Converte para positivo para exibição e serialização JSON
        
        return categorias_despesas
