import logging
import os
import psycopg2
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

dotenv_path = os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(dotenv_path=dotenv_path)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        logging.info("Conexão bem suscedida.")
        return conn


    except psycopg2.OperationalError as e:
        print(f"ERRO CRÍTICO: Não foi possível conectar ao banco de dados. Verifique as credenciais e a rede.")
        print(f"Detalhes do erro: {e}")
        return None
    except Exception as e:
        print(f"ERRO INESPERADO ao conectar ao banco: {e}")
        return None
