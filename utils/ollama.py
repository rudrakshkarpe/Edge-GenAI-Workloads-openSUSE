import ollama 
import os

import streamlit as st

import utils.logs as logs


# NOT USED but kept for the reference
os.environ["OPENAI_API_KEY"] = "sk-abc123" 


from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine


@st.cache_data(show_spinner=False)
def create_ollama_llm(
    model: str, base_url: str, system_prompt: str = None, request_timeout: int = 60
) -> Ollama:

    try:
        # Settings.llm = Ollama(model=model, base_url=base_url, system_prompt=system_prompt, request_timeout=request_timeout)
        Settings.llm = Ollama(
            model=model, base_url=base_url, request_timeout=request_timeout
        )
        logs.log.info("Ollama LLM instance created successfully")
        return Settings.llm
    except Exception as e:
        logs.log.error(f"Error creating Ollama language model: {e}")
        return None


def chat(prompt: str):
    try:
        llm = create_ollama_llm(
            st.session_state["selected_model"],
            st.session_state["ollama_endpoint"],
        )
        stream = llm.stream_complete(prompt)
        for chunk in stream:
            yield chunk.delta
    except Exception as err:
        logs.log.error(f"Error in chat: {err}")
        return


def context_chat(prompt: str, query_engine: RetrieverQueryEngine):
    try:
        stream = query_engine.query(prompt)
        for text in stream.response_gen:
            yield str(text)
    except Exception as err:
        logs.log.error(f"Ollama chat stream error: {err}")
        return


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
