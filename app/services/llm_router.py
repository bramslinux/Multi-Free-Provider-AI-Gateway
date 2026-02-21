import httpx
from fastapi import HTTPException
from app.core.providers import PROVIDERS
from app.core.config import get_env, logger
from typing import List,AsyncIterator
import time
import json


# if you want to use asynchronous mode 
async def call_with_rotation(payload: dict, providers_list: List[str]):

    for provider in providers_list:
        key = get_env(provider)
        if not key:
            logger.info(f"Clé absente pour {provider} passage au suivant")
            continue

        headers = {"Authorization": f"Bearer {key}","Content-Type": "application/json"}
        model = PROVIDERS.get(provider).get("model_name")
        url = PROVIDERS.get(provider).get("url")

        payload_copy = dict(payload)
        payload_copy.setdefault("model", model)
        
        
        try:
            async with httpx.AsyncClient(timeout=None) as client:
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



# if you want to use streaming mode 
async def call_with_rotation_stream(payload: dict, providers_list: List[str]) -> AsyncIterator[str]:
    for provider in providers_list:
        key = get_env(provider)
        if not key:
            continue

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        model = PROVIDERS.get(provider).get("model_name")
        url = PROVIDERS.get(provider).get("url")

        payload_copy = dict(payload)
        payload_copy["model"] = model
        payload_copy["stream"] = True

        try:
            success = False
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", url, headers=headers, json=payload_copy) as response:
                    if response.status_code != 200:
                        error_body = await response.aread()
                        logger.error(f"{provider} error {response.status_code}: {error_body}")
                        continue  # passe au provider suivant

                    success = True
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        while line.startswith("data: "):
                            line = line[6:]
                            if line == "[DONE]":
                                break
                        
                            data = json.loads(line)
                            content = data["choices"][0]["delta"].get("content")
                            if content : 
                                yield f"data :{content}\n\n"
                             
            if success:
                return  # on a eu une réponse complète, on arrête

        except Exception as e:
            logger.error(f"Erreur streaming {provider}: {e}")
            continue

    yield 'data: {"error": "All providers failed"}\n\n'


    