import ollama
import os

import streamlit as st

import utils.logs as logs

# note: not used but required needs to be imported first
os.environ["OPENAI_API_KEY"] = "sk-abc123"

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine

# create ollama client

def create_client(host: str):
  
    try:
        client = ollama.Client(host=host)
        logs.log.info("Ollama chat client created successfully")
        return client
    except Exception as err:
        logs.log.error(f"Failed to create Ollama client: {err}")
        return False


# getting llm models

def get_models():
  
    try:
        chat_client = create_client(st.session_state["ollama_endpoint"])
        data = chat_client.list()
        models = []
        for model in data["models"]:
            models.append(model["name"])

        st.session_state["ollama_models"] = models

        if len(models) > 0:
            logs.log.info("Ollama models loaded successfully")
        else:
            logs.log.warn(
                "Ollama did not return any models. Make sure to download some!"
            )

        return models
    except Exception as err:
        logs.log.error(f"Failed to retrieve Ollama model list: {err}")
        return []

# create ollama instance

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
        logs.log.error(f"Ollama chat stream error: {err}")
        return

# create document chat

def context_chat(prompt: str, query_engine: RetrieverQueryEngine):
    
    try:
        stream = query_engine.query(prompt)
        for text in stream.response_gen:
            # print(str(text), end="", flush=True)
            yield str(text)
    except Exception as err:
        logs.log.error(f"Ollama chat stream error: {err}")
        return
