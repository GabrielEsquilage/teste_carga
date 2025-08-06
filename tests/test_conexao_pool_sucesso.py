import os
import pytest
from dotenv import load_dotenv
import carregador.conexao_banco as pool_manager

@pytest.fixture(scope="module")
def db_config():
    """Carrega as configurações do .env e as retorna como um dicionário."""
    project_root = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path=dotenv_path)

    config = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
    }
    return config

@pytest.fixture(scope="module", autouse=True)
def gerenciador_pool(db_config):
    """Usa a configuração para inicializar e fechar o pool."""
    pool_manager.inicializar_pool(db_config) # Injeta a configuração aqui
    assert pool_manager.db_pool is not None, "O pool de conexões falhou ao ser inicializado."
    yield
    pool_manager.fechar_pool()
    assert pool_manager.db_pool is None, "O pool de conexões não foi fechado corretamente."

@pytest.fixture
def conexao_do_pool():
    """Pega uma conexão do pool e a devolve no final do teste."""
    conn = None
    try:
        conn = pool_manager.get_conexao_do_pool()
        yield conn
    finally:
        if conn:
            pool_manager.devolver_conexao_ao_pool(conn)

def test_conexao_funcional_do_pool(conexao_do_pool):
    """Verifica se a conexão obtida do pool é válida e funcional."""
    conn = conexao_do_pool
    assert conn is not None
    assert not conn.closed
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        resultado = cursor.fetchone()
    assert resultado is not None
    assert resultado[0] == 1
