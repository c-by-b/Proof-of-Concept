# cbyb/providers/groq.py
"""
Groq LLM Provider

Simple provider implementation for Groq API calls.
Used by both Cognitive and Evaluator twins in PoC.
"""

import os
import time
from typing import Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv

from cbyb import LLMProvider

class GroqProvider(LLMProvider):
    """Simple Groq API provider."""
    
    def __init__(self, model: str, use_dev_key: bool = True, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model: Groq model name (e.g., "llama-3.1-8b-instant")
            use_dev_key: Use dev key vs demo key
            **kwargs: Additional model parameters (temperature, max_tokens, etc.)
        """
        load_dotenv()
        
        api_key = os.getenv("GROQ_DEV_KEY" if use_dev_key else "GROQ_DEMO_KEY")
        if not api_key:
            key_type = "GROQ_DEV_KEY" if use_dev_key else "GROQ_DEMO_KEY"
            raise ValueError(f"Missing {key_type} in environment")
            
        self.client = Groq(api_key=api_key)
        self.model = model
        self.default_params = kwargs
        self.token_usage = {"input_tokens": 0, "output_tokens": 0}
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate response from Groq model.
        
        Args:
            prompt: Input prompt
            **kwargs: Override default parameters
        """
        # Merge default params with call-specific params
        params = {**self.default_params, **kwargs}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            
            # Track token usage
            if hasattr(response, 'usage') and response.usage:
                self.token_usage["input_tokens"] += response.usage.prompt_tokens
                self.token_usage["output_tokens"] += response.usage.completion_tokens
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")
    
    def get_token_usage(self) -> Dict[str, int]:
        """Return cumulative token usage statistics."""
        return self.token_usage.copy()
    
    def reset_usage(self) -> None:
        """Reset token usage counters."""
        self.token_usage = {"input_tokens": 0, "output_tokens": 0}