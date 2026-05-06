import logging

class GemService:
    def __init__(self, db):
        self.db = db

    def get_stats(self, schema):
        """Returns basic statistics for the schema dashboard/menu."""
        conn = self.db.get_connection(schema=schema)
        cur = self.db.get_cursor(conn)
        try:
            cur.execute("SELECT COUNT(*) as total FROM tb_aluno")
            alunos = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) as total FROM tb_instrutor")
            instrutores = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) as total FROM tb_instrumento")
            instrumentos = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) as total FROM tb_aula")
            aulas = cur.fetchone()['total']

            return {
                "alunos": alunos,
                "instrutores": instrutores,
                "instrumentos": instrumentos,
                "aulas": aulas
            }
        except Exception as e:
            logging.error(f"Erro ao buscar stats para {schema}: {e}")
            return {"alunos": 0, "instrutores": 0, "instrumentos": 0, "aulas": 0}
        finally:
            cur.close()
            conn.close()

    def get_organizacao_info(self, schema):
        conn = self.db.get_connection()
        cur = self.db.get_cursor(conn)
        try:
            cur.execute("SELECT nome, schema FROM public.tb_organizacao WHERE schema = %s", (schema,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
