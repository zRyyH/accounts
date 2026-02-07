import os
from dotenv import load_dotenv
from pocketbase import PocketBase
from utils import logger

load_dotenv()

_pb = None


def _get_env(key, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Variável de ambiente '{key}' não configurada")
    return value


def _get_pb():
    global _pb
    if _pb is None:
        try:
            url = _get_env("PB_URL")
            email = _get_env("PB_EMAIL")
            password = _get_env("PB_PASSWORD")

            _pb = PocketBase(url)
            _pb.admins.auth_with_password(email, password)
            logger.info("Conectado ao PocketBase")
        except Exception as e:
            logger.error(f"Erro ao conectar ao PocketBase: {e}")
            raise
    return _pb


def _ensure_authenticated():
    try:
        pb = _get_pb()
        if not pb.auth_store.token:
            email = _get_env("PB_EMAIL")
            password = _get_env("PB_PASSWORD")
            pb.admins.auth_with_password(email, password)
            logger.info("Reconectado ao PocketBase")
    except Exception as e:
        logger.error(f"Erro ao verificar autenticação: {e}")
        raise


def get_accounts(collection):
    try:
        _ensure_authenticated()
        pb = _get_pb()
        records = pb.collection(collection).get_full_list(batch=1000)
        valid_records = [
            r for r in records if r.__dict__.get("name") and r.__dict__.get("tag")
        ]
        return valid_records
    except Exception as e:
        logger.error(f"Erro ao buscar contas: {e}")
        return []


def update_account(account_id, data, collection):
    try:
        _ensure_authenticated()
        pb = _get_pb()
        return pb.collection(collection).update(account_id, data)
    except Exception as e:
        logger.error(f"Erro ao atualizar conta {account_id}: {e}")
        return None
