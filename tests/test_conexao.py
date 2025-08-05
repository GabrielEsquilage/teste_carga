import pytest
from carregador.conexao_banco import get_db_connection

@pytest.fixture(scope="module")
def db_connection():
    conn = get_db_connection()
    assert conn is not None, "Falha Teste conexão com banco."
    yield conn

    if not conn.close:
        conn.close()
    assert conn.closed, "Falha na desconexão Teste"
