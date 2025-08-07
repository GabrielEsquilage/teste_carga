import logging
import psycopg2
from carregador.conexao_banco import get_conexao_do_pool, devolver_conexao_ao_pool


log = logging.getLogger(__name__)

def executar_query_db(thread_id: int, caminho_sql: str, params_query: tuple = None, tipo_query: str = 'leitura'):
  log.info(f"[Thread DB {thread_id}] Vai executar a query do arquivo: {caminho_sql}")
  conn = None
  
  try:
    conn = get_conexao_do_pool()
    
    if not conn:
      log.error(f"[Thread DB {thread_id}] Não foi possivel obter conexão do pool. Encerrando thread")
      return
    
    with conn.cursor() as cursor:
      with open(caminho_sql, 'r') as f:
        sql_query = f.read()
        cursor.execute(sql_query, params_query)
        log.info(f"[Thread DB {thread_id}] Query executada com sucesso.")
        
        if tipo_query == 'leitura':
          resultados = cursor.fetchall()
          log.info(f"[Thread DB {thread_id}] {len(resultados)} linhas foram retornadas.")
        elif tipo_query == 'escrita':
          conn.commit()
          log.info(f"[Thread DB {thread_id}] Commit realizado. {cursor.rowcount} linhas afetadas.")
  
  except psycopg2.Error as e:
    log.error(f"[Thread DB {thread_id}] Erro de banco de dados: {e}")
    if conn:
      conn.rollback()
      log.warning(f"[Thread DB {thread_id}] Rollback realizado.")
  
  except FileNotFoundError:
    log.error(f"[Thread DB {thread_id}] ERRO CRÍTICO: Arquivo SQL não encontrado em '{caminho_sql}'")
    
  except Exception as e:
    log.exception(f"[Thread DB {thread_id}] Um erro inesperado ocorreu.")
    if conn:
      conn.rollback()
  
  finally:
    if conn:
      devolver_conexao_ao_pool(conn)
      log.info(f"[Thread DB {thread_id}] Conexão devolvida ao pool.")
