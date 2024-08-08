import ollama 
import os

import streamlit as st

import utils.logs as logs


# NOT USED but kept for the reference
os.environ["OPENAI_API_KEY"] = "sk-abc123" 


from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine

# get clients 

def create_client(host: str):
    try: 
        
        client = ollama.Client(host=host)
        logs.log.info("Ollama chat client created successfully! 🚀")        
        return client
    except Exception as arr:
        logs.log.error(f"Error creating Ollama chat client: {arr}")
        return False


# getting models

def get_models():
    try:
        chat_client = create_client(host=Settings.OLLAMA_HOST)
        data = chat_client.list()
        
        models = []

        for model in data["models"]:
            models.append(model["name"])
        st.session_state["ollama_models"] = models
        
        if len(models) > 0:
            logs.log.info(f"Models fetched successfully: {models}")
            
        else:
            logs.log.error("No models found! Make sure the Ollama server is running and you have it downloaded")
        return models
    
    
    except Exception as arr:
        logs.log.error(f"Failed to retrieve Ollama model list: {arr}")
        return [] 