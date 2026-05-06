import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def criar_banco():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="xbala",
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'db_gem'")
    exists = cur.fetchone()
    if not exists:
        cur.execute("CREATE DATABASE db_gem")
    cur.close()
    conn.close()

def conectar():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="xbala",
        database="db_gem"
    )

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_instrumento (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        ativo BOOLEAN DEFAULT TRUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_comum (
        id SERIAL PRIMARY KEY,
        descricao VARCHAR(150) NOT NULL,
        ativo BOOLEAN DEFAULT TRUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_instrutor (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        telefone VARCHAR(20),
        email VARCHAR(150),
        instrumento_id INT NOT NULL,
        comum_id INT NOT NULL,
        data_batismo DATE NOT NULL,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ativo BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (instrumento_id) REFERENCES tb_instrumento(id),
        FOREIGN KEY (comum_id) REFERENCES tb_comum(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_aluno (
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
        ativo BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (instrumento_id) REFERENCES tb_instrumento(id),
        FOREIGN KEY (instrutor_id) REFERENCES tb_instrutor(id),
        FOREIGN KEY (comum_id) REFERENCES tb_comum(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_responsavel (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        telefone VARCHAR(20),
        email VARCHAR(150),
        ativo BOOLEAN DEFAULT TRUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_aluno_responsavel (
        id SERIAL PRIMARY KEY,
        aluno_id INT NOT NULL,
        responsavel_id INT NOT NULL,
        grau_parentesco VARCHAR(50),
        FOREIGN KEY (aluno_id) REFERENCES tb_aluno(id),
        FOREIGN KEY (responsavel_id) REFERENCES tb_responsavel(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tb_aula (
        id SERIAL PRIMARY KEY,
        aluno_id INT NOT NULL,
        instrutor_id INT NOT NULL,
        instrumento_id INT NOT NULL,
        data_aula TIMESTAMP NOT NULL,
        observacao TEXT,
        presenca BOOLEAN DEFAULT TRUE,
        duracao_minutos INT,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES tb_aluno(id),
        FOREIGN KEY (instrutor_id) REFERENCES tb_instrutor(id),
        FOREIGN KEY (instrumento_id) REFERENCES tb_instrumento(id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def testar_conexao():
    conn = conectar()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        if cur.fetchone()[0] == 1:
            print("Conexão OK")
        cur.close()
        conn.close()

if __name__ == "__main__":
    criar_banco()
    criar_tabelas()
    testar_conexao()