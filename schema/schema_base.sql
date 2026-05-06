CREATE TABLE tb_instrumento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tb_comum (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(150) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tb_instrutor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    instrumento_id INT NOT NULL,
    comum_id INT NOT NULL,
    data_batismo DATE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tb_aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(150),
    instrumento_id INT NOT NULL,
    instrutor_id INT NOT NULL,
    comum_id INT NOT NULL,
    possui_responsavel BOOLEAN DEFAULT FALSE,
    data_batismo DATE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tb_responsavel (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tb_aluno_responsavel (
    id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL,
    responsavel_id INT NOT NULL,
    grau_parentesco VARCHAR(50)
);

CREATE TABLE tb_aula (
    id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL,
    instrutor_id INT NOT NULL,
    instrumento_id INT NOT NULL,
    data_aula TIMESTAMP NOT NULL,
    observacao TEXT,
    presenca BOOLEAN DEFAULT TRUE,
    duracao_minutos INT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);