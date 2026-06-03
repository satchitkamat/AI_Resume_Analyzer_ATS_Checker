import os
import requests

from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

def ask_ollama(prompt):

    response = requests.post(
        "https://ollama.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-oss:120b-cloud",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]