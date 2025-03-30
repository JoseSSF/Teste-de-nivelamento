CREATE DATABASE IF NOT EXISTS ans_dados;
USE ans_dados;

-- Tabela para operadoras de plano ativos
CREATE TABLE IF NOT EXISTS operadoras_de_plano_de_saude_ativas (
    id_operadora INT AUTO_INCREMENT PRIMARY KEY,
    CNPJ INT,
    Razao_Social varchar(500),
    Nome_Fantasia varchar(500),
    Modalidade varchar(150),
    Logradouro varchar(200),
    Numero varchar(10),
    Complemento varchar(200),
    Bairro varchar(100),
    Cidade varchar(100),
    UF varchar(2),
    CEP INT,
    DDD INT,
    Telefone INT,
    Fax INT,
    Endereco_eletronico varchar(100),
    Representante varchar(200),
    Cargo_Representante varchar(100),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS date
);

-- Tabela para demonstrações contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    DATA_MOV date,
    REG_ANS INT,
    CD_CONTA_CONTABIL INT,
    DESCRICAO varchar(500),
    VL_SALDO_INICIAL DECIMAL (10,2),
    VL_SALDO_FINAL DECIMAL (10,2),
);

-- Importando os dados das operadoras
LOAD DATA INFILE '/arquivosBaixados/operadoras/*.csv'
INTO TABLE operadoras_de_plano_de_saude_ativas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, 
Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante, Cargo_Representante, 
Regiao_de_Comercializacao, @Data_Registro_ANS)
SET Data_Registro_ANS = STR_TO_DATE(@Data_Registro_ANS, '%d/%m/%Y');

-- Importando os dados das Demonstrações Contábeis
LOAD DATA INFILE '/arquivosBaixados/demonstracoes/*.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA_MOV, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);

-- Consulta 1: Top 10 operadoras com maiores despesas no último trimestre
SELECT 
    o.Nome_Fantasia AS nome_operadora,
    d.DATA_MOV,
    d.VL_SALDO_FINAL AS despesas_eventos
FROM demonstracoes_contabeis d
JOIN operadoras_de_plano_de_saude_ativas o ON d.REG_ANS = o.CNPJ
WHERE d.DATA_MOV > DATE_SUB((SELECT MAX(d.DATA_MOV) FROM demonstracoes_contabeis), INTERVAL 3 MONTH)
ORDER BY d.VL_SALDO_FINAL DESC
LIMIT 10;

-- Consulta 2: Top 10 operadoras com maiores despesas no último ano
SELECT 
    o.Nome_Fantasia AS nome_operadora,
    YEAR(d.DATA_MOV) AS ano,
    SUM(d.VL_SALDO_FINAL) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras_de_plano_de_saude_ativas o ON d.REG_ANS = o.CNPJ
WHERE YEAR(d.DATA_MOV) = YEAR((SELECT MAX(d.DATA_MOV) FROM demonstracoes_contabeis)) 
GROUP BY o.Nome_Fantasia, YEAR(d.DATA_MOV)
ORDER BY total_despesas DESC
LIMIT 10;
