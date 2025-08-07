import os
import psycopg2
from dotenv import load_dotenv

print("--- INICIANDO SCRIPT DE DEPURAÇÃO DE CONEXÃO ---")

# Carrega o arquivo .env
load_dotenv()

# Passo 1: Imprimir as variáveis que estão sendo lidas do .env
# Verifique se os valores impressos abaixo são EXATAMENTE o que você espera.
print("\nVerificando variáveis de ambiente lidas:")
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

print(f"  DB_HOST: {db_host}")
print(f"  DB_PORT: {db_port}")
print(f"  DB_NAME: {db_name}")
print(f"  DB_USER: {db_user}")
print(f"  DB_PASSWORD: {'*' * len(db_password) if db_password else 'None'}") # Não imprime a senha por segurança

# Passo 2: Tentar conectar usando exatamente essas variáveis
print("\nTentando conectar ao banco de dados...")
conn = None
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("\nSUCESSO! A conexão foi estabelecida com o banco de dados!")
    print(f"Versão do PostgreSQL: {conn.server_version}")

except Exception as e:
    print("\nFALHA! A conexão com o banco de dados falhou.")
    print("\nCausa do erro direto da biblioteca psycopg2:")
    print("-------------------------------------------------")
    print(e)
    print("-------------------------------------------------")

finally:
    if conn:
        conn.close()
        print("\nConexão de teste devidamente fechada.")

print("\n--- FIM DO SCRIPT DE DEPURAÇÃO ---")
