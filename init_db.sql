-- Script para inicialização do banco de dados Primo'sFinCntrl

-- Cria o banco de dados se não existir
CREATE DATABASE IF NOT EXISTS primosfincntrl;

-- Seleciona o banco de dados
USE primosfincntrl;

-- Cria a tabela de categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cor VARCHAR(20) NOT NULL
);

-- Cria a tabela de despesas
CREATE TABLE IF NOT EXISTS despesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data DATE NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Insere categorias padrão se a tabela estiver vazia
INSERT INTO categorias (nome, cor)
SELECT * FROM (
    SELECT 'Alimentação' AS nome, '#FF5733' AS cor UNION ALL
    SELECT 'Transporte', '#33FF57' UNION ALL
    SELECT 'Moradia', '#3357FF' UNION ALL
    SELECT 'Saúde', '#FF33A8' UNION ALL
    SELECT 'Educação', '#33A8FF' UNION ALL
    SELECT 'Lazer', '#A833FF' UNION ALL
    SELECT 'Vestuário', '#FFD700' UNION ALL
    SELECT 'Outros', '#808080'
) AS tmp
WHERE NOT EXISTS (
    SELECT nome FROM categorias
) LIMIT 8;

-- Insere algumas despesas de exemplo
INSERT INTO despesas (descricao, valor, data, categoria_id)
SELECT * FROM (
    SELECT 'Aluguel', -1200.00, CURDATE() - INTERVAL 5 DAY, (SELECT id FROM categorias WHERE nome = 'Moradia') UNION ALL
    SELECT 'Supermercado', -350.50, CURDATE() - INTERVAL 2 DAY, (SELECT id FROM categorias WHERE nome = 'Alimentação') UNION ALL
    SELECT 'Combustível', -150.00, CURDATE() - INTERVAL 1 DAY, (SELECT id FROM categorias WHERE nome = 'Transporte') UNION ALL
    SELECT 'Farmácia', -89.90, CURDATE(), (SELECT id FROM categorias WHERE nome = 'Saúde') UNION ALL
    SELECT 'Cinema', -60.00, CURDATE() - INTERVAL 7 DAY, (SELECT id FROM categorias WHERE nome = 'Lazer')
) AS tmp
WHERE NOT EXISTS (
    SELECT id FROM despesas LIMIT 1
);
