import logging
from psycopg2 import pool, Error

db_pool = None

def inicializar_pool(db_config: dict):
    global db_pool
    if db_pool is None:
        try:
            logging.info("Inicializando o pool de conexões com o banco de dados...")
            db_pool = pool.SimpleConnectionPool(
                minconn=5,
                maxconn=200,
                host=db_config.get('DB_HOST'),
                port=db_config.get('DB_PORT'),
                dbname=db_config.get('DB_NAME'),
                user=db_config.get('DB_USER'),
                password=db_config.get('DB_PASSWORD')
            )
            logging.info("Pool de conexões inicializado com sucesso.")
        except Error as e:
            logging.critical(f"Falha CRÍTICA ao inicializar o pool de conexões: {e}", exc_info=True)
            db_pool = None

def get_conexao_do_pool():
    if db_pool is None:
        logging.error("O pool de conexões não foi inicializado.")
        return None
    try:
        return db_pool.getconn()
    except Exception as e:
        logging.exception("Não foi possível obter uma conexão do pool.")
        return None

def devolver_conexao_ao_pool(conn):
    if db_pool and conn:
        db_pool.putconn(conn)

def fechar_pool():
    global db_pool
    if db_pool:
        db_pool.closeall()
        logging.info("Pool de conexões fechado.")
        db_pool = None
