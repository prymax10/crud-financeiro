#!/bin/bash

# Script para build e deploy da aplicação PrimosFinCntrl na AWS
# Este script deve ser executado na instância EC2 ou em um pipeline CI/CD

set -e

echo "=== PRIMOSFINCNTRL DOCKER BUILD AND DEPLOY ==="
echo "Timestamp: $(date)"

# Configurações
IMAGE_NAME="primosfincntrl"
IMAGE_TAG="latest"
CONTAINER_NAME="primosfincntrl-app"

# Função para verificar se o Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker não está instalado. Instalando..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        sudo usermod -aG docker $USER
        echo "Docker instalado. Faça logout e login novamente."
        exit 1
    fi
}

# Função para parar e remover container existente
cleanup_container() {
    echo "Limpando container existente..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
}

# Função para build da imagem
build_image() {
    echo "Fazendo build da imagem Docker..."
    docker build -t $IMAGE_NAME:$IMAGE_TAG .
    echo "Build concluído!"
}

# Função para executar container
run_container() {
    echo "Executando container..."
    docker run -d \
        --name $CONTAINER_NAME \
        --restart unless-stopped \
        -p 5000:5000 \
        --env-file env.production \
        -e FLASK_ENV=production \
        -e FLASK_APP=app.py \
        $IMAGE_NAME:$IMAGE_TAG
    
    echo "Container iniciado!"
}

# Função para verificar saúde da aplicação
health_check() {
    echo "Verificando saúde da aplicação..."
    for i in {1..30}; do
        if curl -f http://localhost:5000/ping >/dev/null 2>&1; then
            echo "✅ Aplicação está funcionando!"
            return 0
        fi
        echo "Aguardando aplicação inicializar... ($i/30)"
        sleep 2
    done
    echo "❌ Aplicação não está respondendo!"
    return 1
}

# Função para mostrar logs
show_logs() {
    echo "Logs do container:"
    docker logs $CONTAINER_NAME
}

# Execução principal
main() {
    check_docker
    cleanup_container
    build_image
    run_container
    
    if health_check; then
        echo "🎉 Deploy concluído com sucesso!"
        echo "Aplicação disponível em: http://localhost:5000"
        show_logs
    else
        echo "❌ Falha no deploy!"
        show_logs
        exit 1
    fi
}

# Executar script
main "$@" 