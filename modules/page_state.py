import streamlit as st
import utils.logs as logs
from utils.ollama import get_models

class PageState:
    """Manages the application's state and initialization."""

    def __init__(self):
        """Initialize the PageState class."""
        pass

    def initialize(self):
        """Initialize all session state variables."""
        # Sidebar state
        if "sidebar_state" not in st.session_state:
            st.session_state["sidebar_state"] = "expanded"

        # Ollama configuration
        if "ollama_endpoint" not in st.session_state:
            st.session_state["ollama_endpoint"] = "http://localhost:11434"

        if "embedding_model" not in st.session_state:
            st.session_state["embedding_model"] = "Default (bge-large-en-v1.5)"

        # Initialize Ollama models
        if "ollama_models" not in st.session_state:
            try:
                models = get_models()
                st.session_state["ollama_models"] = models
            except Exception:
                st.session_state["ollama_models"] = []

        # Set default model
        if "selected_model" not in st.session_state:
            try:
                if "llama3:8b" in st.session_state["ollama_models"]:
                    st.session_state["selected_model"] = "llama3:8b"
                else:
                    st.session_state["selected_model"] = st.session_state["ollama_models"][0]
            except Exception:
                st.session_state["selected_model"] = None

        # Initialize chat messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{
                "role": "assistant",
                "content": "Alright! Let's get started. Please upload your documents/images or provide a link to a Website/GitHub repository to begin."
            }]

        # Initialize other state variables
        self._initialize_file_states()
        self._initialize_chat_states()
        self._initialize_advanced_states()

    def _initialize_file_states(self):
        """Initialize file-related state variables."""
        if "file_list" not in st.session_state:
            st.session_state["file_list"] = []
        if "github_repo" not in st.session_state:
            st.session_state["github_repo"] = None
        if "websites" not in st.session_state:
            st.session_state["websites"] = []
        if "documents" not in st.session_state:
            st.session_state["documents"] = None

    def _initialize_chat_states(self):
        """Initialize chat-related state variables."""
        if "llm" not in st.session_state:
            st.session_state["llm"] = None
        if "query_engine" not in st.session_state:
            st.session_state["query_engine"] = None
        if "chat_mode" not in st.session_state:
            st.session_state["chat_mode"] = "compact"

    def _initialize_advanced_states(self):
        """Initialize advanced configuration state variables."""
        if "advanced" not in st.session_state:
            st.session_state["advanced"] = False
        if "system_prompt" not in st.session_state:
            st.session_state["system_prompt"] = (
                "You are a sophisticated virtual assistant designed to assist users in "
                "comprehensively understanding and extracting insights from a wide range "
                "of documents at their disposal. Your expertise lies in tackling complex "
                "inquiries and providing insightful analyses based on the information "
                "contained within these documents."
            )
        if "top_k" not in st.session_state:
            st.session_state["top_k"] = 3
        if "chunk_size" not in st.session_state:
            st.session_state["chunk_size"] = 1024
        if "chunk_overlap" not in st.session_state:
            st.session_state["chunk_overlap"] = 200
