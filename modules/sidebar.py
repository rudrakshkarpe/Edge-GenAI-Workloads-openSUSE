import streamlit as st
from utils.ollama import get_models
from components.sources import sources
from components.settings import settings
from components.about import about

class Sidebar:
    """Manages the sidebar components and functionality."""

    def __init__(self):
        """Initialize sidebar components."""
        pass

    def render(self):
        """Render the sidebar with all its components."""
        with st.sidebar:
            self._render_navigation()

    def _render_navigation(self):
        """Render navigation menu in the sidebar."""
        st.title("Navigation")
        
        # Navigation tabs
        tab_sources, tab_settings, tab_about = st.tabs(["📚 Sources", "⚙️ Settings", "ℹ️ About"])
        
        with tab_sources:
            sources()  # This will render the sources component
            
        with tab_settings:
            settings()  # This will render the settings component
            
        with tab_about:
            about()    # This will render the about component

    def _render_model_selection(self):
        """Render model selection section."""
        st.subheader("🤖 Model Selection")
        
        # Ollama endpoint input
        st.text_input(
            "Ollama Endpoint",
            value=st.session_state.get("ollama_endpoint", "http://localhost:11434"),
            key="ollama_endpoint",
            on_change=get_models
        )

        # Model selection
        models = st.session_state.get("ollama_models", [])
        if models:
            st.selectbox(
                "Select Model",
                options=models,
                index=0 if "selected_model" not in st.session_state else models.index(st.session_state["selected_model"]),
                key="selected_model"
            )
        else:
            st.warning("No models available. Please check your Ollama endpoint.")

    def _render_file_upload(self):
        """Render file upload section."""
        st.subheader("📁 Upload Files")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload your documents",
            accept_multiple_files=True,
            type=["pdf", "txt", "doc", "docx"]
        )
        
        if uploaded_files:
            st.session_state["file_list"] = uploaded_files

        # GitHub repository input
        st.text_input(
            "GitHub Repository URL",
            key="github_repo",
            help="Enter the URL of a public GitHub repository"
        )

        # Website URL input
        website_url = st.text_input(
            "Website URL",
            help="Enter the URL of a website to scrape"
        )
        if website_url:
            if "websites" not in st.session_state:
                st.session_state["websites"] = []
            if website_url not in st.session_state["websites"]:
                st.session_state["websites"].append(website_url)

    def _render_advanced_settings(self):
        """Render advanced settings section."""
        st.subheader("⚙️ Advanced Settings")
        
        # Toggle for advanced settings
        show_advanced = st.toggle("Show Advanced Settings", value=st.session_state.get("advanced", False))
        st.session_state["advanced"] = show_advanced

        if show_advanced:
            # System prompt
            st.text_area(
                "System Prompt",
                value=st.session_state.get("system_prompt", ""),
                key="system_prompt"
            )

            # RAG parameters
            st.number_input(
                "Top K",
                min_value=1,
                max_value=10,
                value=st.session_state.get("top_k", 3),
                key="top_k"
            )

            st.number_input(
                "Chunk Size",
                min_value=256,
                max_value=4096,
                value=st.session_state.get("chunk_size", 1024),
                key="chunk_size"
            )

            st.number_input(
                "Chunk Overlap",
                min_value=0,
                max_value=1000,
                value=st.session_state.get("chunk_overlap", 200),
                key="chunk_overlap"
            )
