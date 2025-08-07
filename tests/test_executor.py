import pytest
from carregador.executor_db import executar_query_db
import carregador.conexao_banco as pool_manager

# As fixtures de configuração geral foram movidas para conftest.py

@pytest.fixture
def conexao_para_verificacao():
    """Fornece uma conexão para que o teste possa verificar o resultado no banco."""
    conn = pool_manager.get_conexao_do_pool()
    assert conn is not None, "Falha ao obter conexão do pool para verificação."
    yield conn
    pool_manager.devolver_conexao_ao_pool(conn)

@pytest.fixture
def tabela_de_teste(conexao_para_verificacao):
    """Cria e remove uma tabela temporária para os testes de escrita."""
    nome_tabela = "teste_carga_temp"
    with conexao_para_verificacao.cursor() as cursor:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} (id SERIAL PRIMARY KEY, nome VARCHAR(50));")
        conexao_para_verificacao.commit()
    yield nome_tabela
    with conexao_para_verificacao.cursor() as cursor:
        cursor.execute(f"DROP TABLE {nome_tabela};")
        conexao_para_verificacao.commit()

# --- Testes do Executor ---

def test_execucao_leitura_sucesso(tmp_path, caplog):
    """Verifica se o executor roda uma query de LEITURA com sucesso."""
    sql_file = tmp_path / "query_leitura.sql"
    sql_file.write_text("SELECT 'teste de leitura';")
    
    executar_query_db(thread_id=1, caminho_sql=str(sql_file), tipo_query='leitura')
    
    assert "Query executada com sucesso" in caplog.text
    assert "1 linhas foram retornadas" in caplog.text

def test_execucao_escrita_sucesso(tabela_de_teste, tmp_path, caplog, conexao_para_verificacao):
    """Verifica se o executor roda uma query de ESCRITA com sucesso."""
    sql_file = tmp_path / "query_escrita.sql"
    sql_file.write_text(f"INSERT INTO {tabela_de_teste} (nome) VALUES (%s);")
    
    nome_para_inserir = "automacao_carga"
    params = (nome_para_inserir,)
    
    executar_query_db(thread_id=2, caminho_sql=str(sql_file), params_query=params, tipo_query='escrita')
    
    assert "Commit realizado" in caplog.text
    assert "1 linhas afetadas" in caplog.text
    
    with conexao_para_verificacao.cursor() as cursor:
        cursor.execute(f"SELECT nome FROM {tabela_de_teste} WHERE lower(nome) = lower(%s);", (nome_para_inserir,))
        resultado = cursor.fetchone()
        assert resultado is not None
        assert resultado[0] == nome_para_inserir

def test_falha_arquivo_nao_encontrado(caplog):
    """Verifica se o executor lida com um arquivo SQL inexistente."""
    caminho_falso = "/caminho/que/nao/existe/query.sql"
    executar_query_db(thread_id=3, caminho_sql=caminho_falso)
    
    assert f"Arquivo SQL não encontrado em '{caminho_falso}'" in caplog.text

def test_falha_sintaxe_sql(tmp_path, caplog):
    """Verifica se o executor lida com uma query com erro de sintaxe."""
    sql_file = tmp_path / "query_errada.sql"
    sql_file.write_text("SELEC * FROM tabela_inexistente;")

    executar_query_db(thread_id=4, caminho_sql=str(sql_file))

    assert "Erro de banco de dados" in caplog.text
    assert "Rollback realizado" in caplog.text
