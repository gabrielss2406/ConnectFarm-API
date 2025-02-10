import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect():
    try:
        connection = psycopg2.connect(
            "postgresql://postgres:connectfarm@db.gxnlfyzuqhznrojmkegp.supabase.co:5432/postgres?sslmode=require"
        )
        print("Conexão estabelecida com sucesso.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados sql: {e}")
        raise
