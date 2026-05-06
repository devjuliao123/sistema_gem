import re
import logging
import os

class OrganizationService:
    def __init__(self, db):
        self.db = db
        # Base path relative to this file's directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.schema_sql_path = os.path.join(base_dir, "schema", "schema_base.sql")

    def list_all(self):
        conn = self.db.get_connection()
        cur = self.db.get_cursor(conn)
        try:
            cur.execute("SELECT numero, nome, schema, criado_em FROM public.tb_organizacao ORDER BY numero DESC")
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def create(self, nome):
        if not nome:
            raise ValueError("Nome é obrigatório")

        nome = nome.strip().upper()

        conn = self.db.get_connection()
        cur = conn.cursor()
        try:
            # Check for duplicate name
            cur.execute("SELECT 1 FROM public.tb_organizacao WHERE nome = %s", (nome,))
            if cur.fetchone():
                raise ValueError("Já existe uma organização com este nome")

            # Get next number
            cur.execute("SELECT COALESCE(MAX(numero), 0) + 1 FROM public.tb_organizacao")
            numero = cur.fetchone()[0]
            schema_name = f"org_{str(numero).zfill(4)}"

            # Validate schema name format (extra safety)
            if not re.match(r'^org_\d{4}$', schema_name):
                raise ValueError("Nome de schema inválido gerado")

            # Insert into public table
            cur.execute("""
                INSERT INTO public.tb_organizacao (numero, nome, schema)
                VALUES (%s, %s, %s)
            """, (numero, nome, schema_name))

            # Create schema
            cur.execute(f"CREATE SCHEMA {schema_name}")

            # Run base schema inside the new schema
            with open(self.schema_sql_path, "r", encoding="utf-8") as f:
                sql = f.read()

            cur.execute(f"SET search_path TO {schema_name}")
            cur.execute(sql)

            conn.commit()
            logging.info(f"Organização criada: {nome} ({schema_name})")
            return {"numero": numero, "nome": nome, "schema": schema_name}

        except Exception as e:
            conn.rollback()
            logging.error(f"Erro ao criar organização: {e}")
            raise e
        finally:
            cur.close()
            conn.close()

    def delete(self, numero):
        conn = self.db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT schema FROM public.tb_organizacao WHERE numero = %s", (numero,))
            result = cur.fetchone()
            if not result:
                raise ValueError("Organização não encontrada")

            schema_name = result[0]

            # Delete from public table
            cur.execute("DELETE FROM public.tb_organizacao WHERE numero = %s", (numero,))

            # Drop schema
            cur.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")

            conn.commit()
            logging.info(f"Organização excluída: {numero} ({schema_name})")
            return True
        except Exception as e:
            conn.rollback()
            logging.error(f"Erro ao excluir organização {numero}: {e}")
            raise e
        finally:
            cur.close()
            conn.close()

    def validate_name(self, nome):
        if not nome:
            return False

        nome = nome.strip().upper()

        conn = self.db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM public.tb_organizacao WHERE nome = %s", (nome,))
            return cur.fetchone() is None
        finally:
            cur.close()
            conn.close()

    def schema_exists(self, schema_name):
        if not re.match(r'^[a-z0-9_]+$', schema_name):
            return False

        conn = self.db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()
