import streamlit as st
from utils.ollama import chat, context_chat


def chatbox():
    if prompt := st.chat_input("What help do you need?:"):
        if not st.session_state["query_engine"]:
            st.warning("Please wait for the model to load.")
            st.stop()
            
        st.session_state["messages"].append({"role": "user", "message": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
            
        with st.chat_message("assistant"):
            with st.spinner("Processing...."):
                response = st.write_system(
            
                    context_chat(
                        prompt=prompt, query_engine=st.session_state["query_engine"]
                    )
                    
                )
        st.session_state["messages"].append({"role": "assistant", "message": response})