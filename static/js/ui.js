/**
 * UI.js - Módulo para manipulação da interface do usuário
 * Contém funções para renderizar elementos, manipular eventos e gerenciar o estado da aplicação
 */

// Objeto UI para encapsular todas as funcionalidades da interface
const UI = {
    // Estado da aplicação
    state: {
        despesas: [],
        categorias: [],
        periodoAtual: 'todos',
        periodoAtualEstatisticas: 'todos',
        paginaAtual: 'despesas'
    },
    
    /**
     * Inicializa a interface do usuário
     */
    init: function() {
        console.log('Inicializando UI...');
        
        // Carrega as categorias
        this.carregarCategorias();
        
        // Configura os eventos da interface
        this.configurarEventos();
        
        // Carrega as despesas iniciais
        this.carregarDespesas();
        
        // Define a página inicial como ativa
        this.navegarPara('despesas');
    },
    
    /**
     * Configura os eventos da interface
     */
    configurarEventos: function() {
        // Eventos de navegação
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pagina = e.currentTarget.getAttribute('href').substring(1);
                this.navegarPara(pagina);
            });
        });
        
        // Eventos das abas de período na página de despesas
        document.querySelectorAll('#periodoTabs .nav-link').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Remove a classe active de todas as abas
                document.querySelectorAll('#periodoTabs .nav-link').forEach(t => {
                    t.classList.remove('active');
                });
                
                // Adiciona a classe active na aba clicada
                e.currentTarget.classList.add('active');
                
                // Atualiza o período atual e recarrega as despesas
                this.state.periodoAtual = e.currentTarget.getAttribute('data-periodo');
                this.carregarDespesas();
            });
        });
        
        // Eventos das abas de período na página de estatísticas
        document.querySelectorAll('#periodoTabsEstatisticas .nav-link').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Remove a classe active de todas as abas
                document.querySelectorAll('#periodoTabsEstatisticas .nav-link').forEach(t => {
                    t.classList.remove('active');
                });
                
                // Adiciona a classe active na aba clicada
                e.currentTarget.classList.add('active');
                
                // Atualiza o período atual e recarrega as estatísticas
                this.state.periodoAtualEstatisticas = e.currentTarget.getAttribute('data-periodo');
                this.carregarEstatisticas();
            });
        });
        
        // Evento do botão Nova Despesa
        document.getElementById('btn-nova-despesa').addEventListener('click', () => {
            this.abrirModalDespesa();
        });
        
        // Evento do botão Salvar Despesa
        document.getElementById('btn-salvar-despesa').addEventListener('click', (event) => {
            // Evita múltiplos cliques
            const btnSalvar = event.target;
            if (btnSalvar.disabled) return;
            btnSalvar.disabled = true;
            
            this.salvarDespesa()
                .finally(() => {
                    // Reabilita o botão após a conclusão (sucesso ou erro)
                    setTimeout(() => {
                        btnSalvar.disabled = false;
                    }, 500);
                });
        });
        
        // Evento para fechar o modal e limpar o formulário
        document.getElementById('modal-despesa').addEventListener('hidden.bs.modal', () => {
            document.getElementById('form-despesa').reset();
        });
    },
    
    /**
     * Navega para uma página específica
     * @param {string} pagina - Nome da página para navegar
     */
    navegarPara: function(pagina) {
        // Atualiza o estado
        this.state.paginaAtual = pagina;
        
        // Remove a classe active de todas as páginas e links
        document.querySelectorAll('.content-page').forEach(page => {
            page.classList.remove('active');
        });
        
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        // Adiciona a classe active na página e link correspondentes
        document.getElementById(`${pagina}-page`).classList.add('active');
        document.querySelector(`.sidebar .nav-link[href="#${pagina}"]`).classList.add('active');
        
        // Carrega os dados específicos da página
        if (pagina === 'despesas') {
            this.carregarDespesas();
        } else if (pagina === 'estatisticas') {
            this.carregarEstatisticas();
        }
    },
    
    /**
     * Carrega as categorias do backend
     */
    carregarCategorias: function() {
        CategoriasAPI.obterTodas()
            .then(categorias => {
                this.state.categorias = categorias;
                this.preencherSelectCategorias();
            })
            .catch(error => {
                console.error('Erro ao carregar categorias:', error);
                alert('Erro ao carregar categorias. Verifique o console para mais detalhes.');
            });
    },
    
    /**
     * Preenche o select de categorias no formulário
     */
    preencherSelectCategorias: function() {
        const select = document.getElementById('despesa-categoria');
        
        // Limpa as opções existentes
        select.innerHTML = '<option value="">Selecione uma categoria</option>';
        
        // Adiciona as categorias como opções
        this.state.categorias.forEach(categoria => {
            const option = document.createElement('option');
            option.value = categoria.id;
            option.textContent = categoria.nome;
            option.style.color = categoria.cor;
            select.appendChild(option);
        });

        // Workaround: força o reflow e z-index corretos no <select> dentro do modal
        // para evitar que o menu abra no canto superior esquerdo em alguns ambientes
        select.style.position = 'relative';
        select.style.zIndex = '1060';
        // Força reflow
        void select.offsetHeight;
    },
    
    /**
     * Carrega as despesas do backend
     */
    carregarDespesas: function() {
        DespesasAPI.obterTodas(this.state.periodoAtual)
            .then(despesas => {
                this.state.despesas = despesas;
                this.renderizarDespesas();
                this.atualizarTotalDespesas();
            })
            .catch(error => {
                console.error('Erro ao carregar despesas:', error);
                alert('Erro ao carregar despesas. Verifique o console para mais detalhes.');
            });
    },
    
    /**
     * Renderiza as despesas na tabela
     */
    renderizarDespesas: function() {
        const tbody = document.getElementById('tabela-despesas');
        
        // Limpa o conteúdo atual
        tbody.innerHTML = '';
        
        // Se não houver despesas, exibe uma mensagem
        if (this.state.despesas.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="5" class="text-center">Nenhuma despesa encontrada</td>';
            tbody.appendChild(tr);
            return;
        }
        
        // Renderiza cada despesa
        this.state.despesas.forEach(despesa => {
            const tr = document.createElement('tr');
            
            // Formata o valor como moeda
            const valorFormatado = API_CONFIG.formatarMoeda(despesa.valor);
            
            // Cria o badge para a categoria
            const categoriaBadge = `<span class="badge-categoria" style="background-color: ${despesa.categoria_cor}">${despesa.categoria_nome}</span>`;
            
            // Cria os botões de ação
            const btnEditar = `<button class="btn-acao btn-editar" data-id="${despesa.id}"><i class="fas fa-edit"></i></button>`;
            const btnExcluir = `<button class="btn-acao btn-excluir" data-id="${despesa.id}"><i class="fas fa-trash-alt"></i></button>`;
            
            // Define o conteúdo da linha
            tr.innerHTML = `
                <td>${despesa.descricao}</td>
                <td>${valorFormatado}</td>
                <td>${categoriaBadge}</td>
                <td>${despesa.data}</td>
                <td>${btnEditar} ${btnExcluir}</td>
            `;
            
            // Adiciona eventos aos botões
            tr.querySelector('.btn-editar').addEventListener('click', () => {
                this.editarDespesa(despesa.id);
            });
            
            tr.querySelector('.btn-excluir').addEventListener('click', () => {
                this.confirmarExclusaoDespesa(despesa.id);
            });
            
            tbody.appendChild(tr);
        });
    },
    
    /**
     * Atualiza o total de despesas exibido
     */
    atualizarTotalDespesas: function() {
        // Calcula o total das despesas atuais
        const total = this.state.despesas.reduce((acc, despesa) => acc + despesa.valor, 0);
        
        // Atualiza o elemento na interface
        document.getElementById('total-despesas').textContent = API_CONFIG.formatarMoeda(total);
    },
    
    /**
     * Abre o modal para criar uma nova despesa
     */
    abrirModalDespesa: function() {
        // Define o título do modal
        document.getElementById('modalDespesaLabel').textContent = 'Nova Despesa';
        
        // Limpa o ID da despesa
        document.getElementById('despesa-id').value = '';
        
        // Define a data atual como padrão
        const hoje = new Date().toISOString().split('T')[0];
        document.getElementById('despesa-data').value = hoje;
        
        // Abre o modal
        const modal = new bootstrap.Modal(document.getElementById('modal-despesa'));
        modal.show();
    },
    
    /**
     * Abre o modal para editar uma despesa existente
     * @param {number} id - ID da despesa a ser editada
     */
    editarDespesa: function(id) {
        // Obtém os dados da despesa
        DespesasAPI.obterPorId(id)
            .then(despesa => {
                // Define o título do modal
                document.getElementById('modalDespesaLabel').textContent = 'Editar Despesa';
                
                // Preenche o formulário com os dados da despesa
                document.getElementById('despesa-id').value = despesa.id;
                document.getElementById('despesa-descricao').value = despesa.descricao;
                document.getElementById('despesa-valor').value = Math.abs(despesa.valor); // Valor absoluto para exibição
                document.getElementById('despesa-categoria').value = despesa.categoria_id;
                document.getElementById('despesa-data').value = despesa.data;
                
                // Abre o modal
                const modal = new bootstrap.Modal(document.getElementById('modal-despesa'));
                modal.show();
            })
            .catch(error => {
                console.error('Erro ao obter despesa para edição:', error);
                alert('Erro ao obter despesa para edição. Verifique o console para mais detalhes.');
            });
    },
    
    /**
     * Salva uma despesa (nova ou editada)
     */
    salvarDespesa: function() {
        // Obtém os dados do formulário
        const id = document.getElementById('despesa-id').value;
        const descricao = document.getElementById('despesa-descricao').value;
        const valor = document.getElementById('despesa-valor').value;
        const categoria_id = document.getElementById('despesa-categoria').value;
        const data = document.getElementById('despesa-data').value;
        
        // Validação básica
        if (!descricao || !valor || !categoria_id || !data) {
            alert('Por favor, preencha todos os campos.');
            return Promise.reject('Campos incompletos');
        }
        
        // Prepara os dados da despesa
        const despesa = {
            descricao,
            valor: parseFloat(valor),
            categoria_id: parseInt(categoria_id),
            data
        };
        
        // Decide se é uma criação ou atualização
        const promise = id
            ? DespesasAPI.atualizar(id, despesa)
            : DespesasAPI.criar(despesa);
        
        // Executa a operação
        return promise
            .then(() => {
                // Fecha o modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('modal-despesa'));
                if (modal) modal.hide();
                
                // Remover backdrop/overlay manualmente se necessário
                setTimeout(() => {
                    const backdrop = document.querySelector('.modal-backdrop');
                    if (backdrop) backdrop.remove();
                    document.body.classList.remove('modal-open');
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';
                }, 300);
                
                // Recarrega as despesas
                this.carregarDespesas();
                
                // Se estiver na página de estatísticas, recarrega também
                if (this.state.paginaAtual === 'estatisticas') {
                    this.carregarEstatisticas();
                }
            })
            .catch(error => {
                console.error('Erro ao salvar despesa:', error);
                alert('Erro ao salvar despesa. Verifique o console para mais detalhes.');
                
                // Remover backdrop mesmo em caso de erro
                const backdrop = document.querySelector('.modal-backdrop');
                if (backdrop) backdrop.remove();
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                document.body.style.paddingRight = '';
                
                throw error; // Propaga o erro para que o finally no listener seja executado
            });
    },
    
    /**
     * Confirma a exclusão de uma despesa
     * @param {number} id - ID da despesa a ser excluída
     */
    confirmarExclusaoDespesa: function(id) {
        if (confirm('Tem certeza que deseja excluir esta despesa?')) {
            DespesasAPI.excluir(id)
                .then(() => {
                    // Recarrega as despesas
                    this.carregarDespesas();
                    
                    // Se estiver na página de estatísticas, recarrega também
                    if (this.state.paginaAtual === 'estatisticas') {
                        this.carregarEstatisticas();
                    }
                })
                .catch(error => {
                    console.error('Erro ao excluir despesa:', error);
                    alert('Erro ao excluir despesa. Verifique o console para mais detalhes.');
                });
        }
    },
    
    /**
     * Carrega as estatísticas do backend
     */
    carregarEstatisticas: function() {
        // Carrega o total de despesas
        EstatisticasAPI.obterTotal(this.state.periodoAtualEstatisticas)
            .then(data => {
                document.getElementById('total-despesas-estatisticas').textContent = API_CONFIG.formatarMoeda(data.total);
            })
            .catch(error => {
                console.error('Erro ao carregar total de despesas:', error);
            });
        
        // Carrega as despesas por categoria
        EstatisticasAPI.obterPorCategoria(this.state.periodoAtualEstatisticas)
            .then(dados => {
                this.renderizarGraficoCategorias(dados);
                this.renderizarListaCategorias(dados);
            })
            .catch(error => {
                console.error('Erro ao carregar despesas por categoria:', error);
            });
    },
    
    /**
     * Renderiza o gráfico de despesas por categoria
     * @param {Array} dados - Dados de despesas por categoria
     */
    renderizarGraficoCategorias: function(dados) {
        // Obtém o contexto do canvas
        const ctx = document.getElementById('grafico-categorias').getContext('2d');
        
        // Destrói o gráfico anterior se existir
        if (window.graficoCategoriasChart) {
            window.graficoCategoriasChart.destroy();
        }
        
        // Prepara os dados para o gráfico
        const labels = dados.map(item => item.nome);
        const values = dados.map(item => Math.abs(item.total));
        const colors = dados.map(item => item.cor);
        
        // Adiciona gradientes para melhorar a aparência visual
        const gradients = colors.map((color, index) => {
            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, color);
            gradient.addColorStop(1, this.adjustColor(color, -30)); // versão mais escura da cor
            return gradient;
        });
        
        // Calcula os percentuais para cada categoria
        const total = values.reduce((a, b) => a + b, 0);
        const percentages = values.map(value => Math.round((value / total) * 100));
        
        // Cria o gráfico
        window.graficoCategoriasChart = new Chart(ctx, {
            type: 'doughnut', // mudança para doughnut para melhor aparência
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: gradients,
                    borderColor: '#ffffff',
                    borderWidth: 2,
                    hoverBorderWidth: 4,
                    hoverBackgroundColor: colors,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                cutout: '65%', // tamanho do buraco no meio do gráfico
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 1000,
                    easing: 'easeOutCirc'
                },
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            font: {
                                size: 12,
                                weight: 'bold'
                            },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map(function(label, i) {
                                        const meta = chart.getDatasetMeta(0);
                                        const style = meta.controller.getStyle(i);
                                        const value = chart.data.datasets[0].data[i];
                                        const percentage = percentages[i];
                                        
                                        return {
                                            text: `${label} (${percentage}%)`,
                                            fillStyle: style.backgroundColor,
                                            strokeStyle: style.borderColor,
                                            lineWidth: style.borderWidth,
                                            pointStyle: 'circle',
                                            hidden: !chart.getDataVisibility(i),
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255,255,255,0.9)',
                        titleColor: '#333',
                        bodyColor: '#666',
                        bodyFont: {
                            weight: 'bold'
                        },
                        borderColor: '#ccc',
                        borderWidth: 1,
                        cornerRadius: 10,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw;
                                const percentage = percentages[context.dataIndex];
                                return `${label}: ${API_CONFIG.formatarMoeda(value)} (${percentage}%)`;
                            }
                        }
                    },
                    // Plugin para mostrar as porcentagens diretamente no gráfico
                    datalabels: {
                        color: '#fff',
                        font: {
                            weight: 'bold',
                            size: 14
                        },
                        formatter: (value, ctx) => {
                            const percentage = percentages[ctx.dataIndex];
                            return percentage > 5 ? `${percentage}%` : '';
                        },
                        textShadow: '0 1px 2px rgba(0,0,0,0.6)',
                        anchor: 'center',
                        align: 'center',
                        offset: 0,
                        display: function(context) {
                            return context.dataset.data[context.dataIndex] > 0;
                        }
                    }
                }
            }
        });
    },
    
    // Função auxiliar para ajustar a luminosidade de uma cor
    adjustColor: function(color, amount) {
        return '#' + color.replace(/^#/, '').replace(/../g, color => ('0'+Math.min(255, Math.max(0, parseInt(color, 16) + amount)).toString(16)).substr(-2));
    },
    
    /**
     * Renderiza a lista de despesas por categoria
     * @param {Array} dados - Dados de despesas por categoria
     */
    renderizarListaCategorias: function(dados) {
        const lista = document.getElementById('lista-categorias');
        
        // Limpa o conteúdo atual
        lista.innerHTML = '';

        // Se não houver dados, exibe uma mensagem
        if (dados.length === 0) {
            const item = document.createElement('li');
            item.className = 'list-group-item text-center';
            item.textContent = 'Nenhuma despesa encontrada';
            lista.appendChild(item);
            return;
        }

        // Calcula o total geral
        const totalGeral = dados.reduce((acc, item) => acc + Math.abs(item.total), 0);

        // Renderiza cada categoria
        dados.forEach(categoria => {
            const item = document.createElement('li');
            item.className = 'list-group-item';

            // Formata o valor como moeda
            const valorFormatado = API_CONFIG.formatarMoeda(categoria.total);

            // Calcula o percentual
            const percentual = ((Math.abs(categoria.total) / totalGeral) * 100).toFixed(2);

            // Cria uma barra de progresso para visualização
            const barraProgresso = `
                <div class="progress mt-2" style="height: 8px;">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${percentual}%; background-color: ${categoria.cor}" 
                         aria-valuenow="${percentual}" aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
            `;

            // Define o conteúdo do item com layout melhorado
            item.innerHTML = `
                <div class="categoria-item" data-categoria-id="${categoria.id}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                            <span class="categoria-color-dot me-2" style="background-color: ${categoria.cor}"></span>
                            <span class="categoria-nome fw-bold">${categoria.nome}</span>
                        </div>
                        <div class="text-end">
                            <div class="valor-categoria fw-bold">${valorFormatado}</div>
                            <div class="percentual-categoria text-muted small">${percentual}% do total</div>
                        </div>
                    </div>
                    ${barraProgresso}
                </div>
            `;

            // Adiciona efeito de hover
            item.addEventListener('mouseenter', () => {
                // Destaca a fatia correspondente no gráfico
                if (window.graficoCategoriasChart) {
                    const index = dados.findIndex(c => c.id === categoria.id);
                    if (index !== -1) {
                        window.graficoCategoriasChart.setActiveElements([{datasetIndex: 0, index: index}]);
                        window.graficoCategoriasChart.update();
                    }
                }
                item.classList.add('categoria-hover');
            });

            item.addEventListener('mouseleave', () => {
                // Remove o destaque
                if (window.graficoCategoriasChart) {
                    window.graficoCategoriasChart.setActiveElements([]);
                    window.graficoCategoriasChart.update();
                }
                item.classList.remove('categoria-hover');
            });

            lista.appendChild(item);
        });
    }
};

// Inicializa a UI quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    UI.init();
});
