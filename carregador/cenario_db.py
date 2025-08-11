import threading
import time
import random
import os
import logging
from carregador.executor_db import executar_query_db

log = logging.getLogger(__name__)

parar_threads = threading.Event()

def _get_queries_disponiveis(pasta_assets: str) -> list:
    """Busca todos os arquivos .sql na pasta de assets."""
    try:
        arquivos = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.endswith('.sql')]
        if not arquivos:
            log.warning(f"Nenhum arquivo .sql encontrado na pasta '{pasta_assets}'.")
        return arquivos
    except FileNotFoundError:
        log.error(f"A pasta de assets '{pasta_assets}' não foi encontrada.")
        return []

def _trabalhador_db(thread_id: int, queries: list, max_iteracoes: int = None):
    """
    Função que cada thread executará em loop, rodando queries aleatórias.
    max_iteracoes: usado apenas para testes, limita o número de iterações no loop.
    """
    log.info(f"[Thread {thread_id}] Iniciada.")
    iteracoes = 0

    while not parar_threads.is_set():
        if not queries:
            log.error(f"[Thread {thread_id}] Nenhuma query para executar. Encerrando.")
            break

        try:
            caminho_sql_aleatorio = random.choice(queries)
            log.info(f"[Thread {thread_id}] Selecionou a query: {os.path.basename(caminho_sql_aleatorio)}")

            executar_query_db(
                thread_id=thread_id,
                caminho_sql=caminho_sql_aleatorio,
                tipo_query='leitura'
            )

            time.sleep(random.uniform(1.0, 5.0))

        except Exception as e:
            log.exception(f"[Thread {thread_id}] Erro inesperado no loop do trabalhador: {e}")
            time.sleep(5)

        iteracoes += 1
        if max_iteracoes and iteracoes >= max_iteracoes:
            log.info(f"[Thread {thread_id}] Máximo de iterações atingido. Encerrando.")
            break

    log.info(f"[Thread {thread_id}] Sinal de parada recebido. Encerrando.")

def rodar_cenario_db(num_threads: int, duracao_segundos: int, pasta_assets: str):
    """Orquestra o teste de carga no banco de dados."""
    log.info(f"--- INICIANDO CENÁRIO DE TESTE DE CARGA NO BANCO ---")
    log.info(f"Configuração: {num_threads} usuários | Duração: {duracao_segundos} segundos")

    queries = _get_queries_disponiveis(pasta_assets)
    if not queries:
        log.critical("Nenhuma query encontrada. Abortando teste.")
        return

    parar_threads.clear()
    threads = []

    for i in range(num_threads):
        thread = threading.Thread(target=_trabalhador_db, args=(i + 1, queries), name=f"TrabalhadorDB-{i+1}")
        threads.append(thread)
        thread.start()

    log.info(f"Todas as {num_threads} threads foram iniciadas. O teste está em andamento...")

    time.sleep(duracao_segundos)

    log.info("Tempo de teste esgotado. Enviando sinal de parada para as threads...")
    parar_threads.set()

    for thread in threads:
        thread.join()

    log.info("--- CENÁRIO DE TESTE DE CARGA NO BANCO FINALIZADO ---")
