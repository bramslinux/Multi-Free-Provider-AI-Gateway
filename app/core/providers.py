PROVIDERS = {
    "openrouter": 
        {"env_name": "OPENROUTER_KEY", "url" : "https://openrouter.ai/api/v1/chat/completions", "model_name" : "nvidia/nemotron-nano-9b-v2:free"},
   
    "huggingface": 
        {"env_name": "HF_KEY", "url" : "https://router.huggingface.co/v1/chat/completions", "model_name" : "zai-org/GLM-5:novita"},
   
    "mistral": 
        {"env_name": "MISTRAL_KEY", "url" : "https://api.mistral.ai/v1/chat/completions" ,"model_name" : "mistral-large-latest"},
   
    "groq": 
        {"env_name": "GROQ_KEY", "url" : "https://api.groq.com/openai/v1/chat/completions" ,"model_name" : "openai/gpt-oss-120b"},
   
    "poe": 
        {"env_name": "POE_KEY", "url" : "https://api.poe.com/v1/chat/completions" ,"model_name" : "assistant"},
   
    "nvidia": 
        {"env_name": "NVIDIA_KEY", "url" : "https://integrate.api.nvidia.com/v1/chat/completions" ,"model_name" : "meta/llama-3.3-70b-instruct"}}