import streamlit as st

from utils.ollama import chat, context_chat


def chatbox():
    if prompt := st.chat_input("How can I help?"):

        if not st.session_state["query_engine"]:
            st.warning("Please confirm settings and upload files before proceeding.")
            st.stop()

        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = st.write_stream(
                    # chat(
                    #     prompt=prompt
                    # )
                    context_chat(
                        prompt=prompt, query_engine=st.session_state["query_engine"]
                    )
                )
        st.session_state["messages"].append({"role": "assistant", "content": response})
