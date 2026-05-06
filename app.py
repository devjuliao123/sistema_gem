from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

DB_NAME = "db_gem"
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "xbala"
}

def conectar(db=DB_NAME):
    conn = psycopg2.connect(database=db, **DB_CONFIG)
    conn.autocommit = True
    return conn

def criar_database():
    conn = psycopg2.connect(database="postgres", **DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME}")
    cur.close()
    conn.close()

def carregar_sql():
    with open("schema/schema_base.sql", "r", encoding="utf-8") as f:
        return f.read()

def executar_schema(conn, schema):
    cur = conn.cursor()
    sql = carregar_sql()
    cur.execute(f"SET search_path TO {schema}")
    cur.execute(sql)
    conn.commit()
    cur.close()

def proximo_numero():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(numero),0)+1 FROM public.tb_organizacao")
    numero = cur.fetchone()[0]
    cur.close()
    conn.close()
    return numero

def inicializar():
    criar_database()
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.tb_organizacao (
            id SERIAL PRIMARY KEY,
            numero INT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            schema TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("SELECT COUNT(*) FROM public.tb_organizacao")
    total = cur.fetchone()[0]

    if total == 0:
        numero = 1
        schema = "org_0001"

        cur.execute("""
            INSERT INTO public.tb_organizacao (numero, nome, schema)
            VALUES (%s, %s, %s)
        """, (numero, "IGREJA PADRÃO", schema))

        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        executar_schema(conn, schema)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/organizacoes")
def listar():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT numero, nome, schema FROM public.tb_organizacao ORDER BY numero DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"numero": r[0], "nome": r[1], "schema": r[2]}
        for r in rows
    ])

@app.route("/criar", methods=["POST"])
def criar():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "nome obrigatório"}), 400

    conn = conectar()
    cur = conn.cursor()

    numero = proximo_numero()
    schema = f"org_{str(numero).zfill(4)}"

    try:
        cur.execute("""
            INSERT INTO public.tb_organizacao (numero, nome, schema)
            VALUES (%s, %s, %s)
        """, (numero, nome, schema))

        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        executar_schema(conn, schema)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"ok": True, "schema": schema})

    except Exception as e:
        conn.close()
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    inicializar()
    app.run(debug=True)