import os
import logging
import requests
from schemathesis import openapi, Case, checks
from schemathesis.hooks import HookContext

log = logging.getLogger(__name__)

schema = None

def _obter_token_jwt() -> str | None:
    base_url = os.getenv('API_BASE_URL_ERP')
    auth_endpoint = os.getenv('API_AUTH_ENDPOINT')
    user = os.getenv('API_USER')
    password = os.getenv('API_PASSWORD')

    login_url = f"{base_url}{auth_endpoint}"
    credentials = {'username': user, 'password': password}
    
    log.info(f"A tentar autenticar em {login_url} com o utilizador '{user}'...")

    try:
        response = requests.post(login_url, json=credentials)
        response.raise_for_status()

        token = response.json().get('token')

        if not token:
            log.error("Autenticação bem sucedida, mas o token nao foi encontrado na resposta.")
            return None

        log.info("Token JWT obtido com sucesso!")
        return token

    except requests.exceptions.RequestException as e:
        log.critical(f"Falha Critica na autenticação: {e}")
        if e.response is not None:
            log.critical(f"Status da Resposta: {e.response.status_code}")
            log.critical(f"Corpo da Resposta: {e.response.text}")
        return None

def rodar_cenario_api():
    global schema
    log.info("--Iniciando cenário de Teste de API--")

    if schema is None:
        doc_url = os.getenv('API_BASE_DOC_ERP')
        log.info(f"Carregando especificação da API de {doc_url}")
        try:
            schema = openapi.from_url(doc_url)
        except Exception as e:
            log.critical(f"Não foi possivel carregar o schema da API: {e}")
            return
    
    token = _obter_token_jwt()
    if not token:
        log.critical("Não foi possivel obter o token de autenticação. Abortando teste da API.")
        return

    @schema.hook("before_generate_case")
    def add_auth_header(context: HookContext, case: Case):
        case.headers = case.headers or {}
        case.headers["Authorization"] = f"Bearer {token}"

    runner = schema.runner(
        base_url=os.getenv('API_BASE_URL_ERP'),
        checks=checks.load_all_checks(),
        workers_num=4
    )

    runner.execute()

    log.info("-- Cenario de teste de API finalizado --")
