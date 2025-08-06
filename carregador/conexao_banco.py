import logging
from psycopg2 import pool, Error

# O módulo não se preocupa mais com .env ou os
# A configuração de logging pode continuar aqui
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

db_pool = None

# A função agora recebe a configuração como um dicionário
def inicializar_pool(db_config: dict):
    global db_pool
    if db_pool is None:
        try:
            logging.info("Inicializando o pool de conexões com o banco de dados...")
            # Usa os valores do dicionário recebido, em vez de os.getenv()
            db_pool = pool.SimpleConnectionPool(
                minconn=5,
                maxconn=50,
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

# As outras funções permanecem iguais
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
