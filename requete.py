"""
import requests

url = "http://127.0.0.1:8000/api/chat/stream"

payload = {
    "messages": [
        {"role": "user", "content": " quelle est la capitale du burkina faso "}
    ]
}

response = requests.post(url, json=payload)

print("STATUS:", response.status_code)

try:
    print(response.json())
except Exception:
    print("Réponse brute:")
    print(response.text)

 """

import requests

url = "http://127.0.0.1:8000/api/chat/stream"
payload = {"messages": [{"role": "user", "content": "Qui est l'homme le plus riche du monde ?"}]}

with requests.post(url, json=payload, stream=True) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode()[6:], end="", flush=True)