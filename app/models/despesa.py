#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para manipulação de despesas no banco de dados usando SQLAlchemy
"""

from datetime import datetime, timedelta
from app.models.database import db, Despesa as DespesaModel, Categoria as CategoriaModel
import sqlalchemy as sa

class Despesa:
    """
    Classe para manipulação de despesas no banco de dados usando SQLAlchemy
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
        # Query base
        query = DespesaModel.query
        
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
        
        # Ordena por data mais recente
        despesas = query.order_by(DespesaModel.data.desc()).all()
        
        # Converte em dicionários e formata as datas para formato brasileiro
        result = []
        for despesa in despesas:
            despesa_dict = despesa.to_dict()
            # Formata a data para o formato brasileiro
            data = datetime.strptime(despesa_dict['data'], '%Y-%m-%d')
            despesa_dict['data'] = data.strftime('%d/%m/%Y')
            result.append(despesa_dict)
        
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
        despesa = DespesaModel.query.get(despesa_id)
        return despesa.to_dict() if despesa else None
    
    @staticmethod
    def criar(dados):
        """
        Cria uma nova despesa no banco de dados
        
        Args:
            dados (dict): Dados da despesa (descricao, valor, data, categoria_id)
        
        Returns:
            int: ID da despesa criada
        """
        try:
            # Garante que o valor seja negativo (despesa)
            valor = float(dados['valor'])
            if valor > 0:
                valor = -valor
            
            # Converte a data de string para objeto date
            data_obj = datetime.strptime(dados['data'], '%Y-%m-%d').date()
            
            # Cria o objeto despesa
            nova_despesa = DespesaModel(
                descricao=dados['descricao'],
                valor=valor,
                data=data_obj,
                categoria_id=dados['categoria_id']
            )
            
            # Salva no banco de dados
            db.session.add(nova_despesa)
            db.session.commit()
            
            return nova_despesa.id
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar despesa: {e}")
            raise
    
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
        try:
            despesa = DespesaModel.query.get(despesa_id)
            if not despesa:
                return False
            
            # Garante que o valor seja negativo (despesa)
            valor = float(dados['valor'])
            if valor > 0:
                valor = -valor
            
            # Converte a data de string para objeto date
            data_obj = datetime.strptime(dados['data'], '%Y-%m-%d').date()
            
            # Atualiza os campos
            despesa.descricao = dados['descricao']
            despesa.valor = valor
            despesa.data = data_obj
            despesa.categoria_id = dados['categoria_id']
            
            # Salva as alterações
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar despesa: {e}")
            return False
    
    @staticmethod
    def excluir(despesa_id):
        """
        Exclui uma despesa do banco de dados
        
        Args:
            despesa_id (int): ID da despesa
        
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            despesa = DespesaModel.query.get(despesa_id)
            if not despesa:
                return False
            
            # Remove a despesa
            db.session.delete(despesa)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao excluir despesa: {e}")
            return False
