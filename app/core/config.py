import os
from dotenv import load_dotenv
from app.core.providers import PROVIDERS
load_dotenv()

def get_env(provider_name):
    provider_key = PROVIDERS[provider_name].get("env_name")
    return os.getenv(provider_key)
    

import logging

# Configuration de base
logging.basicConfig(
    level=logging.INFO,  # Niveau minimal de log
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Logger
logger = logging.getLogger(__name__)