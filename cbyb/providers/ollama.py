# cbyb/providers/ollama_provider.py

import requests
from cbyb import LLMProvider

class OllamaProvider:
    def __init__(self, model: str, host="http://localhost:11434", **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model: Ollama hosted model name
            host: Ollama localhost server
            **kwargs: Additional model parameters (temperature, max_tokens, etc.)
        """
        
        self.model_name = model
        self.host = host
        self.default_params = kwargs
        self.token_usage = {"input_tokens": 0, "output_tokens": 0}

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate response from model.
        
        Args:
            prompt: Input prompt
            **kwargs: Override default parameters
        """
        # Merge default params with call-specific params
        params = {**self.default_params, **kwargs}
        
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "options": {
                    "temperature": params["temperature"]
                    "num_predict": params["max_temperature"]
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    
    def get_token_usage(self) -> Dict[str, int]:
        """Return cumulative token usage statistics."""
        return self.token_usage.copy()
    
    def reset_usage(self) -> None:
        """Reset token usage counters."""
        self.token_usage = {"input_tokens": 0, "output_tokens": 0}