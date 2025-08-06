# cbyb/providers/ollama_provider.py

import requests

class OllamaProvider:
    def __init__(self, model_name="gpt-oss:20b", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "options": {
                    "temperature": 0.0,
                    "num_predict": max_tokens
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]