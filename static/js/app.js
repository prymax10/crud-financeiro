/**
 * App.js - Arquivo principal da aplicação
 * Responsável por inicializar a aplicação quando o DOM estiver pronto
 */

// Função para inicializar a aplicação
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, inicializando aplicação...');
    
    // Inicializa a UI
    UI.init();
    
    // Configura a navegação por hash na URL
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.substring(1);
        if (hash && (hash === 'despesas' || hash === 'estatisticas')) {
            UI.navegarPara(hash);
        }
    });
    
    // Verifica se há um hash na URL inicial
    const hash = window.location.hash.substring(1);
    if (hash && (hash === 'despesas' || hash === 'estatisticas')) {
        UI.navegarPara(hash);
    }
    
    // Define a data atual como padrão no formulário
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('despesa-data').value = hoje;
    
    // Inicializa os tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
