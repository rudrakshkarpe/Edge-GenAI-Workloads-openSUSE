import ollama
import os

import streamlit as st

import utils.logs as logs

# note: not used but required needs to be imported first
os.environ["OPENAI_API_KEY"] = "sk-abc123"

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine

from typing import Generator, Optional

class OllamaChat:
    """Handles interaction with the Ollama API for chat functionality.
    
    This class manages the Ollama client creation, model management,
    and chat operations.
    """

    def __init__(self):
        """Initialize the Ollama chat handler."""
        self.client = None

    def create_client(self, base_url: str) -> Optional[ollama.Client]:
        """Create an Ollama client instance.
        
        Args:
            base_url (str): The Ollama server host address
            
        Returns:
            Optional[ollama.Client]: The created client or None if failed
        """
        try:
            self.client = ollama.Client(base_url=base_url)
            logs.log.info("Ollama chat client created successfully")
            return self.client
        except Exception as err:
            logs.log.error(f"Failed to create Ollama client: {err}")
            return None

    @staticmethod
    def create_ollama_llm(
        model: str,
        base_url: str,
        system_prompt: str = None,
        request_timeout: int = 60
    ) -> Optional[Ollama]:
        """Create an Ollama language model instance.
        
        Args:
            model (str): The model name to use
            base_url (str): The base URL for the Ollama service
            system_prompt (str, optional): System prompt for the model
            request_timeout (int, optional): Request timeout in seconds
            
        Returns:
            Optional[Ollama]: The created LLM instance or None if failed
        """
        try:
            Settings.llm = Ollama(
                model=model,
                base_url=base_url,
                request_timeout=request_timeout
            )
            logs.log.info("Ollama LLM instance created successfully")
            return Settings.llm
        except Exception as e:
            logs.log.error(f"Error creating Ollama language model: {e}")
            return None

    def chat(self, prompt: str) -> Generator[str, None, None]:
        """Generate a chat response stream.
        
        Args:
            prompt (str): The user's input prompt
            
        Yields:
            str: Response text chunks
        """
        try:
            llm = self.create_ollama_llm(
                st.session_state["selected_model"],
                st.session_state["ollama_endpoint"],
            )
            stream = llm.stream_complete(prompt)
            for chunk in stream:
                yield chunk.delta
        except Exception as err:
            logs.log.error(f"Ollama chat stream error: {err}")
            return

# getting llm models

def get_models(endpoint: Optional[str] = None):
    """Get models from specified Ollama endpoint or try both system and container endpoints"""
    models = []
    endpoints = [
        "http://localhost:11434",  # System Ollama
        "http://localhost:11435",  # Container Ollama
    ] if endpoint is None else [endpoint]
    
    for url in endpoints:
        try:
            chat_client = OllamaChat().create_client(url)
            data = chat_client.list()
            for model in data['models']:
                models.append({
                    'model': model['model'],
                    'endpoint': url
                })
            logs.log.info(f"Successfully loaded models from {url}")
        except Exception as err:
            logs.log.warning(f"Failed to retrieve models from {url}: {err}")
    
    return models

# create document chat

def context_chat(prompt: str, query_engine: RetrieverQueryEngine, endpoint: str = None):
    """Chat function that can use either Ollama instance"""
    try:
        # Use the specified endpoint or default to system Ollama
        endpoint = endpoint or "http://localhost:11434"
        # Your existing chat code with endpoint configuration
        stream = query_engine.query(prompt)
        for text in stream.response_gen:
            yield str(text)
    except Exception as err:
        logs.log.error(f"Ollama chat stream error: {err}")
        return
