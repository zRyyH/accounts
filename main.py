import os
import sys
import time
from dotenv import load_dotenv
from pocket import get_accounts, update_account
from scrapper import check_account
from utils import logger

load_dotenv()


def _get_env(key, default=None):
    value = os.getenv(key, default)
    if value is None:
        logger.error(f"Variável de ambiente '{key}' não configurada")
        sys.exit(1)
    return value


def _validate_config():
    required_vars = [
        "PB_URL",
        "PB_EMAIL",
        "PB_PASSWORD",
        "API_TOKEN",
        "COLLECTION_NAME",
    ]

    for var in required_vars:
        if not os.getenv(var):
            logger.error(f"Variável de ambiente '{var}' obrigatória não configurada")
            sys.exit(1)

    logger.info("Configurações validadas com sucesso")


def _process_account(account, collection):
    try:
        name = account.__dict__.get("name")
        tag = account.__dict__.get("tag")
        account_id = account.__dict__.get("id")

        if not name or not tag or not account_id:
            logger.warning("Conta com dados inválidos encontrada")
            return

        data = check_account(name, tag)

        if not data:
            logger.warning(f"{name}#{tag} → Sem dados disponíveis")
            return

        if data == 24:
            update_account(account_id, {"status": "INATIVO"}, collection)
            logger.info(f"{name}#{tag} → INATIVO")
            return

        data["status"] = "ATIVO"
        result = update_account(account_id, data, collection)

        if result:
            logger.info(
                f"{name}#{tag} → ATIVO | Rank: {data['last_rank']} | Última atividade: {data['last_activity']}"
            )

    except Exception as e:
        logger.error(f"Erro ao processar conta: {e}")


def main():
    _validate_config()

    collection = _get_env("COLLECTION_NAME")
    interval = int(_get_env("CHECK_INTERVAL", "10"))

    logger.info("Iniciando monitoramento de contas Valorant")
    logger.info(f"Intervalo entre verificações: {interval}s")

    while True:
        try:
            accounts = get_accounts(collection)

            if not accounts:
                logger.warning("Nenhuma conta encontrada")
                time.sleep(interval)
                continue

            logger.info(f"Processando {len(accounts)} contas...")

            for account in accounts:
                try:
                    _process_account(account, collection)
                    time.sleep(interval)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"Erro ao processar conta: {e}")
                    continue

        except KeyboardInterrupt:
            logger.info("Encerrando aplicação...")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            logger.info(f"Aguardando {interval * 2}s antes de retomar...")
            time.sleep(interval * 2)


if __name__ == "__main__":
    main()
