import pytest
import carregador.conexao_banco as pool_manager

# Reutiliza a fixture de configuração do outro arquivo ou a redefine se preferir
# Para manter o arquivo independente, vamos redefini-la aqui
@pytest.fixture
def db_config_valida():
    # Esta fixture só é necessária para ter uma base para a configuração inválida
    return {
        'DB_HOST': '104.198.51.109',
        'DB_PORT': '5432',
        'DB_NAME': 'erp',
        'DB_USER': 'erp_user',
        'DB_PASSWORD': 'senha-so-para-teste'
    }

def test_falha_inicializacao_com_senha_invalida(db_config_valida):
    """Testa se a inicialização do pool falha corretamente com uma senha errada."""
    if pool_manager.db_pool is not None:
        pool_manager.fechar_pool()

   
    config_invalida = db_config_valida.copy()
    config_invalida['DB_PASSWORD'] = 'senha-com-certeza-errada'


    pool_manager.inicializar_pool(config_invalida)

    assert pool_manager.db_pool is None
