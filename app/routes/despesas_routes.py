#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rotas para manipulação de despesas
"""

from flask import Blueprint, request, jsonify
from app.models.despesa import Despesa

# Criação do blueprint para as rotas de despesas
bp = Blueprint('despesas', __name__)

@bp.route('/', methods=['GET'])
def listar_despesas():
    """
    Lista todas as despesas, com opção de filtro por período
    """
    periodo = request.args.get('periodo')
    despesas = Despesa.listar(periodo)
    return jsonify(despesas)

@bp.route('/<int:despesa_id>', methods=['GET'])
def obter_despesa(despesa_id):
    """
    Obtém uma despesa específica pelo ID
    """
    despesa = Despesa.obter_por_id(despesa_id)
    if despesa:
        return jsonify(despesa)
    return jsonify({"error": "Despesa não encontrada"}), 404

@bp.route('/', methods=['POST'])
def criar_despesa():
    """
    Cria uma nova despesa
    """
    dados = request.json
    
    # Validação básica dos dados
    campos_obrigatorios = ['descricao', 'valor', 'data', 'categoria_id']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"error": f"Campo obrigatório ausente: {campo}"}), 400
    
    try:
        despesa_id = Despesa.criar(dados)
        return jsonify({"id": despesa_id, "message": "Despesa criada com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:despesa_id>', methods=['PUT'])
def atualizar_despesa(despesa_id):
    """
    Atualiza uma despesa existente
    """
    dados = request.json
    
    # Validação básica dos dados
    campos_obrigatorios = ['descricao', 'valor', 'data', 'categoria_id']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"error": f"Campo obrigatório ausente: {campo}"}), 400
    
    # Verifica se a despesa existe
    despesa = Despesa.obter_por_id(despesa_id)
    if not despesa:
        return jsonify({"error": "Despesa não encontrada"}), 404
    
    try:
        sucesso = Despesa.atualizar(despesa_id, dados)
        if sucesso:
            return jsonify({"message": "Despesa atualizada com sucesso"})
        return jsonify({"error": "Erro ao atualizar despesa"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:despesa_id>', methods=['DELETE'])
def excluir_despesa(despesa_id):
    """
    Exclui uma despesa
    """
    # Verifica se a despesa existe
    despesa = Despesa.obter_por_id(despesa_id)
    if not despesa:
        return jsonify({"error": "Despesa não encontrada"}), 404
    
    try:
        sucesso = Despesa.excluir(despesa_id)
        if sucesso:
            return jsonify({"message": "Despesa excluída com sucesso"})
        return jsonify({"error": "Erro ao excluir despesa"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
