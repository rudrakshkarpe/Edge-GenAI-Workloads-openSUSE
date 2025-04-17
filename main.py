from typing import Generator
import time
import streamlit as st

from modules.chatbox import ChatBox
from modules.header import PageHeader
from modules.sidebar import Sidebar
from modules.page_config import PageConfig
from modules.page_state import PageState

class LLMLocalizationApp:
    """Main application class for LLM Localization.
    
    This class serves as the entry point for the Streamlit application and coordinates
    all major components including the chat interface, sidebar, and page configuration.
    """

    def __init__(self):
        """Initialize the application components."""
        # Initialize state first
        self.page_state = PageState()
        self.page_state.initialize()  # Initialize state before other components
        
        # Then initialize other components
        self.page_config = PageConfig()
        self.header = PageHeader()
        self.sidebar = Sidebar()
        self.chatbox = ChatBox()

    def display_welcome_message(self, msg: str) -> Generator[str, None, None]:
        """Display an animated welcome message.
        
        Args:
            msg (str): The message to display
            
        Yields:
            str: Each character of the message for animation
        """
        for char in msg:
            time.sleep(0.20)
            st.markdown(
                f"<h1 style='text-align: center; color: #000000;'>{msg}</h1>",
                unsafe_allow_html=True,
            )
            yield char

    def run(self):
        """Run the main application loop."""
        # Initialize app state
        self.page_state.initialize()
        
        # Configure page
        self.page_config.configure()
        self.header.render()

        # Display existing messages
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        # Setup sidebar and chat interface
        self.sidebar.render()
        self.chatbox.render()

def initialize_session_state():
    if "ollama_endpoint" not in st.session_state:
        st.session_state["ollama_endpoint"] = "http://localhost:11434"  # Default to system Ollama
    if "ollama_models" not in st.session_state:
        st.session_state["ollama_models"] = []

def main():
    initialize_session_state()
    app = LLMLocalizationApp()
    app.run()

if __name__ == "__main__":
    main()
