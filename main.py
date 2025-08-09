import os
import logging
from dotenv import load_dotenv

from carregador.conexao_banco import inicializar_pool, fechar_pool
from carregador.cenario_db import rodar_cenario_db

# --- Configurações do Teste de Carga ---
NUMERO_DE_USUARIOS_SIMULTANEOS = 40
DURACAO_DO_TESTE_EM_SEGUNDOS = 60
PASTA_DE_ASSETS_SQL = 'assets'

def executar_teste_carga():
    """Ponto de entrada principal da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log = logging.getLogger(__name__)
  
    log.info("Carregando configurações do arquivo .env...")
    load_dotenv()
  
    db_config = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
    }
  
    if not all(db_config.values()):
        log.critical("Erro: Uma ou mais variáveis de ambiente não foram definidas. Verifique o .env")
        return
  
    inicializar_pool(db_config)
  
    try:
        rodar_cenario_db(
            num_threads=NUMERO_DE_USUARIOS_SIMULTANEOS,
            duracao_segundos=DURACAO_DO_TESTE_EM_SEGUNDOS,
            pasta_assets=PASTA_DE_ASSETS_SQL
        )
    
    except KeyboardInterrupt:
        log.warning("Teste Interrompido pelo Usuário (Ctrl + C).")
    except Exception as e:
        log.exception(f"Ocorreu um erro crítico durante a execução: {e}")
    finally:
        log.info("Encerrando a aplicação e fechando o pool de conexões.")
        fechar_pool()
    
if __name__ == '__main__':
    executar_teste_carga()
