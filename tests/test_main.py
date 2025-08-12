import sys
import os
from unittest.mock import patch

# Adiciona a pasta raiz ao path para garantir que 'import main' funcione
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from main import executar_teste_carga


@patch('main.inicializar_pool')
@patch('main.rodar_cenario_db') 
@patch('main.fechar_pool')
@patch('main.load_dotenv')
def test_main_orquestracao_completa(mock_load_dotenv, mock_fechar_pool, mock_rodar_cenario, mock_inicializar_pool, mocker):
    """
    Testa se a função principal 'executar_teste_carga' chama todas as
    etapas de orquestração na ordem correta.
    """
    mocker.patch('os.getenv', return_value="valor_falso_para_teste")

    executar_teste_carga()

    mock_load_dotenv.assert_called_once()
    mock_inicializar_pool.assert_called_once()
    mock_rodar_cenario.assert_called_once()
    mock_fechar_pool.assert_called_once()


@patch('main.inicializar_pool')
@patch('main.rodar_cenario_db')
@patch('main.fechar_pool')
@patch('main.load_dotenv')
def test_main_fecha_pool_mesmo_com_erro_no_cenario(mock_load_dotenv, mock_fechar_pool, mock_rodar_cenario, mock_inicializar_pool, mocker):
    """
    Testa o comportamento CRÍTICO: garante que o pool é fechado
    mesmo que o cenário de teste levante uma exceção.
    """
    mocker.patch('os.getenv', return_value="valor_falso_para_teste")

    erro_simulado = Exception("Erro durante o teste de carga!")
    mock_rodar_cenario.side_effect = erro_simulado

    executar_teste_carga()
    
    mock_inicializar_pool.assert_called_once()
    mock_rodar_cenario.assert_called_once()
    mock_fechar_pool.assert_called_once()
