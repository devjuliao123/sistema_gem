import psycopg2
from psycopg2.extras import RealDictCursor
import logging

class Database:
    def __init__(self, db_config):
        self.config = db_config
        self.db_name = db_config.get("database", "db_gem")
        self._ensure_db_exists()
        self._run_migrations()

    def _get_connection(self, dbname=None):
        config = self.config.copy()
        if dbname:
            config["database"] = dbname
        return psycopg2.connect(**config)

    def _ensure_db_exists(self):
        conn = self._get_connection("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.db_name,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.db_name}")
        cur.close()
        conn.close()

    def _run_migrations(self):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            # Create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.tb_organizacao (
                    id SERIAL PRIMARY KEY,
                    numero INT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    schema TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Ensure UNIQUE constraint on nome
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'tb_organizacao_nome_key'
                    ) THEN
                        ALTER TABLE public.tb_organizacao ADD CONSTRAINT tb_organizacao_nome_key UNIQUE (nome);
                    END IF;
                END $$;
            """)

            # Ensure indexes
            cur.execute("CREATE INDEX IF NOT EXISTS idx_org_numero ON public.tb_organizacao(numero)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_org_schema ON public.tb_organizacao(schema)")

            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(f"Migration error: {e}")
            raise e
        finally:
            cur.close()
            conn.close()

    def get_connection(self, schema=None):
        conn = self._get_connection(self.db_name)
        if schema:
            cur = conn.cursor()
            # search_path is safe here if schema is validated by regex in service
            cur.execute(f"SET search_path TO {schema}, public")
            cur.close()
        return conn

    def get_cursor(self, conn):
        return conn.cursor(cursor_factory=RealDictCursor)
