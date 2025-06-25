/**
 * API.js - Módulo para comunicação com o backend
 * Contém funções para realizar requisições AJAX para a API REST
 */

// Configuração base da API
const API_CONFIG = {
    // Usa API_BASE_URL definido em api-url-config.js para funcionar em qualquer ambiente
    BASE_URL: 'http://crud-finance-alb-233355946.us-east-2.elb.amazonaws.com/api'
,
    
    // Função auxiliar para formatar valores monetários
    formatarMoeda: function(valor) {
        // Sempre usa o valor absoluto para remover o sinal negativo
        return Math.abs(valor).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    },
    
    // Função auxiliar para formatar datas para exibição
    formatarData: function(dataString) {
        if (!dataString) return '';
        
        // Se já estiver no formato brasileiro (dd/mm/yyyy), retorna como está
        if (dataString.includes('/')) return dataString;
        
        // Converte de yyyy-mm-dd para Date e depois para dd/mm/yyyy
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR');
    },
    
    // Função auxiliar para formatar datas para o backend (yyyy-mm-dd)
    formatarDataBackend: function(dataString) {
        if (!dataString) return '';
        
        // Se já estiver no formato ISO (yyyy-mm-dd), retorna como está
        if (dataString.includes('-') && !dataString.includes('/')) return dataString;
        
        // Converte de dd/mm/yyyy para yyyy-mm-dd
        const partes = dataString.split('/');
        if (partes.length === 3) {
            return `${partes[2]}-${partes[1]}-${partes[0]}`;
        }
        
        // Fallback: retorna a data atual
        const hoje = new Date();
        return hoje.toISOString().split('T')[0];
    }
};

/**
 * Módulo para manipulação de despesas
 */
const DespesasAPI = {
    /**
     * Obtém todas as despesas do backend
     * @param {string} periodo - Filtro de período (diario, semanal, mensal, anual, todos)
     * @returns {Promise} Promise com os dados das despesas
     */
    obterTodas: function(periodo = null) {
        let url = `${API_CONFIG.BASE_URL}/despesas/`;
        
        // Adiciona o filtro de período se fornecido e não for "todos"
        if (periodo && periodo !== 'todos') {
            url += `?periodo=${periodo}`;
        }
        
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter despesas: ${response.status}`);
                }
                return response.json();
            });
    },
    
    /**
     * Obtém uma despesa específica pelo ID
     * @param {number} id - ID da despesa
     * @returns {Promise} Promise com os dados da despesa
     */
    obterPorId: function(id) {
        return fetch(`${API_CONFIG.BASE_URL}/despesas/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter despesa: ${response.status}`);
                }
                return response.json();
            });
    },
    
    /**
     * Cria uma nova despesa
     * @param {Object} despesa - Dados da despesa
     * @returns {Promise} Promise com o resultado da operação
     */
    criar: function(despesa) {
        return fetch(`${API_CONFIG.BASE_URL}/despesas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(despesa)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao criar despesa: ${response.status}`);
            }
            return response.json();
        });
    },
    
    /**
     * Atualiza uma despesa existente
     * @param {number} id - ID da despesa
     * @param {Object} despesa - Novos dados da despesa
     * @returns {Promise} Promise com o resultado da operação
     */
    atualizar: function(id, despesa) {
        return fetch(`${API_CONFIG.BASE_URL}/despesas/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(despesa)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao atualizar despesa: ${response.status}`);
            }
            return response.json();
        });
    },
    
    /**
     * Exclui uma despesa
     * @param {number} id - ID da despesa
     * @returns {Promise} Promise com o resultado da operação
     */
    excluir: function(id) {
        return fetch(`${API_CONFIG.BASE_URL}/despesas/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao excluir despesa: ${response.status}`);
            }
            return response.json();
        });
    }
};

/**
 * Módulo para manipulação de categorias
 */
const CategoriasAPI = {
    /**
     * Obtém todas as categorias
     * @returns {Promise} Promise com os dados das categorias
     */
    obterTodas: function() {
        return fetch(`${API_CONFIG.BASE_URL}/categorias/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter categorias: ${response.status}`);
                }
                return response.json();
            });
    },
    
    /**
     * Obtém uma categoria específica pelo ID
     * @param {number} id - ID da categoria
     * @returns {Promise} Promise com os dados da categoria
     */
    obterPorId: function(id) {
        return fetch(`${API_CONFIG.BASE_URL}/categorias/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter categoria: ${response.status}`);
                }
                return response.json();
            });
    }
};

/**
 * Módulo para obtenção de estatísticas
 */
const EstatisticasAPI = {
    /**
     * Obtém o total de despesas para um determinado período
     * @param {string} periodo - Filtro de período (diario, semanal, mensal, anual, todos)
     * @returns {Promise} Promise com o total de despesas
     */
    obterTotal: function(periodo = null) {
        let url = `${API_CONFIG.BASE_URL}/estatisticas/total`;
        
        // Adiciona o filtro de período se fornecido e não for "todos"
        if (periodo && periodo !== 'todos') {
            url += `?periodo=${periodo}`;
        }
        
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter total de despesas: ${response.status}`);
                }
                return response.json();
            });
    },
    
    /**
     * Obtém as despesas agrupadas por categoria para um determinado período
     * @param {string} periodo - Filtro de período (diario, semanal, mensal, anual, todos)
     * @returns {Promise} Promise com as despesas por categoria
     */
    obterPorCategoria: function(periodo = null) {
        let url = `${API_CONFIG.BASE_URL}/estatisticas/por-categoria`;
        
        // Adiciona o filtro de período se fornecido e não for "todos"
        if (periodo && periodo !== 'todos') {
            url += `?periodo=${periodo}`;
        }
        
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao obter despesas por categoria: ${response.status}`);
                }
                return response.json();
            });
    }
};
