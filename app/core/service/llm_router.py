import httpx
from fastapi import HTTPException
from app.core.providers import PROVIDERS
from app.core.config import get_env, logger
from typing import Dict, List
import time

# Recuperation de la clef depuis .env
def get_key(provider_name: str):
    key = PROVIDERS.get(provider_name, {}).get("env_name")
    real_key = get_env(key)
    return real_key


#Methode de rotation automatique de clef + logging 
async def call_with_rotation(payload: dict, providers_list: List[str]):

    for provider in providers_list:
        key = get_key(provider)
        if not key:
            logger.info(f"Clé absente pour {provider} passage au suivant")
            continue

        headers = {"Authorization": f"Bearer {key}","Content-Type": "application/json"}
        model = PROVIDERS.get(provider).get("model_name")
        url = PROVIDERS.get(provider).get("url")

        payload_copy = dict(payload)
        payload_copy.setdefault("model", model)
        
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                #logger.info(f"envoie de la requete HTTP  avec les parametre suivant url :{url} - headers :{headers} - payload :{payload}")
                response = await client.post(url, headers=headers, json=payload_copy)

            if response.status_code == 200:
                 content = response.json()
                 if "error" in content:
                      logger.warning(f"Erreur côté modèle {provider}: {content['error']}")
                      continue

            elif response.status_code == 429:
                logger.warning(f"Quota atteint pour {provider}, passage au suivant")
                PROVIDERS.pop(provider)
                continue

            elif response.status_code in (500, 502, 503, 504):
                logger.warning(f"Erreur serveur pour {provider}, retry rapide")
                time.sleep(1)
                continue

            response.raise_for_status()
            choice = content.get("choices", [{}])[0]

            if "message" in choice:
                    message = choice["message"].get("content")
            elif "text" in choice:
                    message = choice.get("text")

            return {
                "provider": provider,
                "response": message or content
            }

        except Exception as e:
            logger.error(f"Erreur réseau pour {provider}: {e}")
            continue

    raise HTTPException(
        status_code=503,
        detail=f"Tous les providers ont échoué"
    )
