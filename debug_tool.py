import os
import logging
from dotenv import load_dotenv
from psycopg2 import pool, Error

# Configura um logging básico para vermos as mensagens
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("--- INICIANDO SCRIPT DE DEPURAÇÃO DO POOL DE CONEXÕES ---")

load_dotenv()

db_pool = None
try:
    print("\nTentando inicializar o pool de conexões...")
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

    print("\n✅ ✅ ✅ SUCESSO! O POOL de conexões foi inicializado! ✅ ✅ ✅")

    print("\nTentando pegar e devolver uma conexão do pool...")
    # Pega uma conexão do pool
    conn = db_pool.getconn()
    print(f"  - Conexão obtida. Status: {'Aberta' if not conn.closed else 'Fechada'}")

    # Devolve a conexão ao pool
    db_pool.putconn(conn)
    print("  - Conexão devolvida ao pool com sucesso.")

except Error as e:
    print("\n❌ ❌ ❌ FALHA! Não foi possível inicializar o POOL de conexões. ❌ ❌  ❌")
    print("\nCausa do erro direto da biblioteca psycopg2:")
    print("-------------------------------------------------")
    print(e)
    print("-------------------------------------------------")

finally:
    if db_pool:
        db_pool.closeall()
        print("\nPool de conexões devidamente fechado.")

print("\n--- FIM DO SCRIPT DE DEPURAÇÃO DO POOL ---")
