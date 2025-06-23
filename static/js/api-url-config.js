/**
 * api-url-config.js - Define a URL base da API de forma dinâmica
 * Permite que o sistema funcione tanto em ambiente local quanto em produção
 */

// Função para obter a URL base da API
function getApiBaseUrl() {
    // Em produção: usa o mesmo domínio (window.location.origin)
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `${window.location.origin}/api`;
    } 
    // Em desenvolvimento local: usa a porta específica do backend
    else {
        // Porta do backend em ambiente de desenvolvimento (padrão: 5000)
        return `${window.location.origin}/api`;
    }
}

// URL base da API para uso em todo o código
const API_BASE_URL = getApiBaseUrl();

// Log para debug
console.log('API Base URL configurada:', API_BASE_URL);
