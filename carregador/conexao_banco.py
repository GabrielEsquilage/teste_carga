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
            error_message = f"""
            FALHA CRÍTICA NA CONEXÃO COM O BANCO.
            A thread não poderá prosseguir. Verifique os seguintes pontos:
            1. O IP/Host '{os.getenv('DB_HOST')}' está correto e acessível?
            2. A porta '{os.getenv('DB_PORT')}' está aberta no firewall?
            3. O usuário '{os.getenv('DB_USER')}' e a senha estão corretos?
            4. O banco de dados '{os.getenv('DB_NAME')}' realmente existe?
            Detalhes originais do erro: {e}
            """
            logging.critical(error_message)
            return None

    except Exception as e:
        logging.exception("Ocorreu um erro inesperado ao tentar conectar...")
        return None
