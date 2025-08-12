import os
import pytest
import logging
from dotenv import load_dotenv
import carregador.conexao_banco as pool_manager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@pytest.fixture(scope="session")
def db_config():
    """
    Carrega as configs do .env uma vez por sessão de teste e retorna um dict.
    """
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
    assert all(config.values()), "Uma ou mais variáveis de ambiente não foram carregadas do .env"
    return config

@pytest.fixture(scope="function", autouse=True)
def gerenciador_pool(db_config):
    """
    Usa a config para inicializar o pool no início de toda a sessão de testes
    e o fecha no final. 'autouse=True' garante que ele sempre será ativado.
    """
    pool_manager.inicializar_pool(db_config)
    yield
    pool_manager.fechar_pool()
