import streamlit as st
from utils.ollama import OllamaChat, context_chat

class ChatBox:
    """Handles the chat interface and message processing.
    
    This class manages the chat input/output, message history, and interaction
    with the Ollama chat backend.
    """

    def __init__(self):
        """Initialize the chat interface."""
        self.ollama_chat = OllamaChat()

    def render(self):
        """Render the chat interface and handle user input."""
        if prompt := st.chat_input("How can I help?"):
            if not st.session_state.get("query_engine"):
                st.warning("Please confirm settings and upload files before proceeding.")
                st.stop()

            self._process_message(prompt)

    def _process_message(self, prompt: str):
        """Process a user message and generate a response.
        
        Args:
            prompt (str): The user's input message
        """
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = st.write_stream(
                    context_chat(
                        prompt=prompt,
                        query_engine=st.session_state["query_engine"]
                    )
                )
        st.session_state["messages"].append({"role": "assistant", "content": response})
