#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rotas para manipulação de categorias
"""

from flask import Blueprint, jsonify
from app.models.categoria import Categoria

# Criação do blueprint para as rotas de categorias
bp = Blueprint('categorias', __name__)

@bp.route('/', methods=['GET'])
def listar_categorias():
    """
    Lista todas as categorias disponíveis
    """
    categorias = Categoria.listar()
    return jsonify(categorias)

@bp.route('/<int:categoria_id>', methods=['GET'])
def obter_categoria(categoria_id):
    """
    Obtém uma categoria específica pelo ID
    """
    categoria = Categoria.obter_por_id(categoria_id)
    if categoria:
        return jsonify(categoria)
    return jsonify({"error": "Categoria não encontrada"}), 404
