#!/bin/bash
# entrypoint.sh

echo "Inicializando o banco de dados..."
python init_db.py

echo "Iniciando a aplicação Flask..."
python app.py
