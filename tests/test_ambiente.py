import os
from dotenv import load_dotenv

def test_se_variaveis_de_ambiente_sao_carregadas():
    """
    Este teste verifica se o arquivo .env está sendo lido
    corretamente dentro do ambiente de execução do pytest.
    """
    print("\n--- Iniciando verificação de variáveis de ambiente no Pytest ---")

    # Define o caminho para o .env de forma robusta
    # Pega o caminho deste arquivo de teste -> vai para a pasta 'tests' -> sobe um nível para a raiz do projeto
    project_root = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(project_root, '.env')

    print(f"Caminho procurado para o .env: {dotenv_path}")

    # Tenta carregar o arquivo
    foi_carregado = load_dotenv(dotenv_path=dotenv_path)
    print(f"Arquivo .env foi encontrado e carregado? {foi_carregado}")

    # Imprime os valores que o pytest está 'enxergando'
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')

    print(f"Valor de DB_HOST visto pelo teste: {db_host}")
    print(f"Valor de DB_USER visto pelo teste: {db_user}")

    # Agora, as asserções. Se alguma falhar, saberemos que as variáveis não foram carregadas.
    assert foi_carregado, "O arquivo .env não foi encontrado ou não pôde ser carregado."
    assert db_host is not None, "A variável DB_HOST está como None."
    assert db_user is not None, "A variável DB_USER está como None."

    print("--- Verificação de variáveis de ambiente finalizada com sucesso! ---")
