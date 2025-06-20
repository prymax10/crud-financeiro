#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rotas para obtenção de estatísticas
"""

from flask import Blueprint, request, jsonify
from app.models.estatistica import Estatistica

# Criação do blueprint para as rotas de estatísticas
bp = Blueprint('estatisticas', __name__)

@bp.route('/total', methods=['GET'])
def total_despesas():
    """
    Retorna o total de despesas para um determinado período
    """
    periodo = request.args.get('periodo')
    total = Estatistica.total_despesas(periodo)
    return jsonify({"total": total})

@bp.route('/por-categoria', methods=['GET'])
def despesas_por_categoria():
    """
    Retorna as despesas agrupadas por categoria para um determinado período
    """
    periodo = request.args.get('periodo')
    dados = Estatistica.despesas_por_categoria(periodo)
    return jsonify(dados)
