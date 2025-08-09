import pytest
from unittest.mock import patch
from carregador import cenario_db

def test_get_queries_disponiveis_com_sucesso(tmp_path):
    """Verifica se a função encontra os arquivos .sql corretamente."""
    (tmp_path / "q1.sql").touch()
    (tmp_path / "q2.sql").touch()
    (tmp_path / "leia_me.txt").touch()

    queries = cenario_db._get_queries_disponiveis(str(tmp_path))

    assert len(queries) == 2
    assert any("q1.sql" in q for q in queries)
    assert any("q2.sql" in q for q in queries)

def test_get_queries_pasta_inexistente(caplog):
    """Verifica se a função lida com uma pasta que não existe."""
    queries = cenario_db._get_queries_disponiveis("/pasta/que/nao/existe")

    assert queries == []
    assert "não foi encontrada" in caplog.text


#revisar função de teste, está em loop intermitente


def test_rodar_cenario_banco_logica_principal(mocker, tmp_path, caplog):
    """
    Testa a lógica principal de 'rodar_cenario_db' usando mocks.
    Verifica se as threads são criadas e se o executor é chamado.
    """
    (tmp_path / "dummy_query.sql").touch()
    
    mock_thread = mocker.patch('threading.Thread')
    mocker.patch('time.sleep')
    mock_executor = mocker.patch('carregador.cenario_db.executar_query_db')

    cenario_db.rodar_cenario_db(
        num_threads=5,
        duracao_segundos=1,
        pasta_assets=str(tmp_path)
    )
    
    assert mock_thread.call_count == 5, "Deveria ter tentado criar 5 threads"
    
    primeira_chamada_thread = mock_thread.call_args_list[0]
    assert primeira_chamada_thread.kwargs['target'] == cenario_db._trabalhador_db
    
    assert cenario_db.parar_threads.is_set()

    assert "CENÁRIO DE TESTE DE CARGA NO BANCO FINALIZADO" in caplog.text
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Para testar o trabalhador isoladamente, precisamos garantir que o sinal
    # de parada esteja limpo, senão o loop 'while' dele não executa.
    
    cenario_db.parar_threads.clear() # <--- LINHA ADICIONADA
    mock_executor.reset_mock() 
    
    args_primeira_thread = primeira_chamada_thread.kwargs['args']
    
    cenario_db._trabalhador_db(
        thread_id=args_primeira_thread[0],
        queries=args_primeira_thread[1]
    )
    
    assert mock_executor.called, "A função _trabalhador_db não chamou o executar_query_db"

