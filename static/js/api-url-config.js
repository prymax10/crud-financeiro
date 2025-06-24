/**
 * api-url-config.js - Define a URL base da API de forma dinâmica
 * Permite que o sistema funcione tanto em ambiente local quanto em produção
 */

// Função para obter a URL base da API
function getApiBaseUrl() {
    // Verifica se está em ambiente de produção (AWS)
    if (window.location.hostname === 'crud-finance-alb-233355946.us-east-2.elb.amazonaws.com') {
        // Usa o DNS do Load Balancer
        return `http://crud-finance-alb-233355946.us-east-2.elb.amazonaws.com/api`;
    }
    // Verifica se é outro ambiente de produção
    else if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `${window.location.origin}/api`;
    } 
    // Em desenvolvimento local: usa a porta local
    else {
        return 'http://localhost:5000/api';
    }
}

// URL base da API para uso em todo o código
const API_BASE_URL = getApiBaseUrl();

// Log para debug
console.log('API Base URL configurada:', API_BASE_URL);
