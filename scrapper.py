import os
import time
from urllib.parse import quote
from dotenv import load_dotenv
import requests
from utils import transform_date, logger

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_REGION = os.getenv("API_REGION", "na")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", "5"))


def _api_request(url):
    if not API_TOKEN:
        logger.error("API_TOKEN não configurado")
        return None

    headers = {"Authorization": API_TOKEN}

    for attempt in range(API_MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=API_TIMEOUT)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:
                logger.warning(f"Rate limit atingido, aguardando {API_RETRY_DELAY}s")
                time.sleep(API_RETRY_DELAY)
                continue

            try:
                error_data = response.json()
                if "errors" in error_data and len(error_data["errors"]) > 0:
                    return {"code": error_data["errors"][0]["code"]}
            except Exception:
                pass

            return None

        except requests.Timeout:
            logger.warning(f"Timeout na requisição (tentativa {attempt + 1}/{API_MAX_RETRIES})")
            if attempt < API_MAX_RETRIES - 1:
                time.sleep(API_RETRY_DELAY)
        except requests.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            if attempt < API_MAX_RETRIES - 1:
                time.sleep(API_RETRY_DELAY)
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return None

    return None


def check_account(name, tag):
    try:
        name_encoded = quote(name)
        tag_encoded = quote(tag)

        base_url = "https://api.henrikdev.xyz/valorant"
        url_matches = f"{base_url}/v3/matches/{API_REGION}/{name_encoded}/{tag_encoded}"
        url_mmr = f"{base_url}/v2/mmr/{API_REGION}/{name_encoded}/{tag_encoded}"

        matches = _api_request(url_matches)
        mmr = _api_request(url_mmr)

        if not matches or not mmr:
            return None

        if matches.get("code") == 24 or mmr.get("code") == 24:
            return 24

        if not matches.get("data") or not mmr.get("data"):
            return None

        match_data = matches["data"][0]
        mmr_data = mmr["data"]["current_data"]

        return {
            "last_activity": transform_date(match_data["metadata"]["game_start_patched"]),
            "last_rank": mmr_data["currenttierpatched"],
        }

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Erro ao processar dados da API para {name}#{tag}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao verificar {name}#{tag}: {e}")
        return None
