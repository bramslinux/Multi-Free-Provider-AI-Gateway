# Multi-Free-Provider AI Gateway
API FastAPI pour interroger plusieurs modèles LLM (OpenRouter, HuggingFace, Gemini, etc.) 
avec rotation automatique des clés et monitoring des quotas.

## Installation

1. Cloner le projet
```bash
git clone https://github.com/bramslinux/Multi-Free-Provider-AI-Gateway.git
```
## Environnement virtuel
2. Créer et activer l’environnement virtuel
   
```bash
python -m venv env
source env/bin/activate  # Linux / macOS
env\Scripts\activate     # Windows
```
## Dépendances
3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### Configuration

4. Crée un fichier .env à la racine du projet.
5. Ajoute tes clés API LLM, par exemple :

## Configuration

6. Crée un fichier `.env` à la racine du projet
7. Ajoute tes clés API LLM, par exemple :

        OPENROUTER_KEY=xxxxx
        HF_KEY=xxxxx
        MISTRAL_KEY=xxxxx

9. urls  providers API:
            1.  [POE](https://poe.com/api)
            2.  [NVIDIA](https://build.nvidia.com/settings/api-keys)
            3.  [MISTRAL](https://admin.mistral.ai/organization/api-keys)
            4.  [GEMINI](https://aistudio.google.com/api-keys)
            5.  [GROQ](https://console.groq.com/keys)
            6.  [OPENROUTER](https://openrouter.ai/settings/keys)
            7.  [HGGINGFACE](https://huggingface.co/settings/tokens)

## Lancer le serveur
8. uvicorn app.main:app --reload --reload-include ".env"
