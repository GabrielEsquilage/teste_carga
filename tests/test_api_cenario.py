import pytest
import requests
from unittest.mock import MagicMock

# Importa o módulo que queremos testar
from carregador import cenario_api

def test_obter_token_sucesso(mocker):
    """Testa se a função _obter_token_jwt lida com uma resposta de sucesso."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'token': 'meu_token_secreto'}
    
    mock_post = mocker.patch('requests.post', return_value=mock_response)
    
    token = cenario_api._obter_token_jwt()
    
    assert token == 'meu_token_secreto'
    mock_post.assert_called_once()

def test_obter_token_falha(mocker, caplog):
    """Testa se a função _obter_token_jwt lida com uma falha de autenticação."""
    # CORREÇÃO: Simula a exceção correta que o código espera
    mock_post = mocker.patch('requests.post')
    mock_post.side_effect = requests.exceptions.RequestException("Simulação de falha de rede")

    token = cenario_api._obter_token_jwt()
    
    assert token is None
    assert "Falha Critica na autenticação" in caplog.text

def test_rodar_cenario_api_orquestracao_completa(mocker, caplog):
    """Testa a lógica principal de 'rodar_cenario_api' usando mocks."""
    mock_obter_token = mocker.patch('carregador.cenario_api._obter_token_jwt', return_value="token-valido")
    
    mock_schema = MagicMock()
    mock_runner = MagicMock()
    mock_schema.runner.return_value = mock_runner
    # CORREÇÃO: O patch deve apontar para onde a função é USADA
    mock_from_uri = mocker.patch('carregador.cenario_api.schemathesis.from_uri', return_value=mock_schema)
    
    cenario_api.rodar_cenario_api()
    
    mock_from_uri.assert_called_once()
    mock_obter_token.assert_called_once()
    
    mock_schema.runner.assert_called_once()
    mock_runner.execute.assert_called_once()

    assert "Cenario de teste de API finalizado" in caplog.text

def test_rodar_cenario_api_falha_no_token(mocker, caplog):
    """Testa se o cenário para corretamente se não conseguir obter um token."""
    mocker.patch('carregador.cenario_api._obter_token_jwt', return_value=None)
    
    # Prepara um mock para o runner para garantir que ele não seja executado
    mock_runner = MagicMock()
    # "Moca" a cadeia de chamadas: schemathesis.from_uri(...).runner(...).execute()
    mocker.patch('carregador.cenario_api.schemathesis.from_uri.return_value.runner.return_value', mock_runner)
    
    cenario_api.rodar_cenario_api()
    
    assert "Abortando teste da API" in caplog.text
    # CORREÇÃO: Verifica se o método 'execute' do runner não foi chamado
    mock_runner.execute.assert_not_called()
