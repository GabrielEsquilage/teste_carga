import threading
import time
import random
import os
import logging
from carregador.executor_db import executar_query_db

log = logging.getLogger(__name__)

parar_threads = threading.Event()

def _get_queries_avaliable(pasta_assets: str) -> list:
  try:
    arquivos = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.endswith('.sql')]
    if not arquivos:
      log.warning(f"nenhum arquivo .sql encontrado na pasta '{pasta_assets}'.")
    return arquivos
  except FileNotFoundError:
    log.error(f"A pasta de assets '{pasta_assets}' não foi encontrada.")
    return []
  
def _worker_db(thread_id: int, queries: list):
  log.info(f"[Thread {thread_id}] Iniciada.")
  while not parar_threads.is_set():
    if not queries:
      log.error(f"[Thread {thread_id}] Nenhuma Query para Executar, Encerrando...")
      break
    
    try:
      caminho_sql_aleatorio = random.choice(queries)
      log.info(f"[Thread {thread_id}] Selecionou a quary: {os.path.basename(caminho_sql_aleatorio)}")
      
      executar_query_db(
        thread_id=thread_id,
        caminho_sql=caminho_sql_aleatorio,
        tipo_query='leitura'  
      )
      
      time.sleep(random.uniform(1.0, 5.0))
      
    except Exception as e:
      log.exception(f"[Thread {thread_id}] Erro inesperado no loop do worker: {e}")
      time.sleep(5)
      
  log.info(f"[Thread {thread_id}] Sinal de parada recebido. Encerrando.")

def rodar_scenario_db(num_threads: int, duracao_segundos: int, pasta_assets: str):
  
  log.info(f"--- INICIANDO CENÁRIO DE TESTE DE CARGA NO BANCO ---")
  log.info(f"Configuração: {num_threads} usuários | Duração: {duracao_segundos} segundos")
  
  queries = _get_queries_avaliable(pasta_assets)
  if not queries:
    log.critical("nenhuma query encontrada, abortando teste")
    return
  parar_threads.clear()
  threads = []
  
  for i in range(num_threads):
    thread = threading.Thread(target=_worker_db, args=(i + 1, queries))
    threads.append(thread)
    thread.start()
    
  log.info(f"Todas as {num_threads} threads foram iniciadas. O teste está em andamento...")
  
  time.sleep(duracao_segundos)
  
  log.info("Tempo de teste esgotado. Enviando sinal de parada para as threads...")
  parar_threads.set()
    
    # Espera todas as threads terminarem suas últimas tarefas
  for thread in threads:
        thread.join()
        
  log.info("--- CENÁRIO DE TESTE DE CARGA NO BANCO FINALIZADO ---")