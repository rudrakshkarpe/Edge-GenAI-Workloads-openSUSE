import streamlit as st


def set_page_header():
    gradient_text_html = """
        <style>
        .gradient-text {
            font-weight: bold;
            background: -webkit-linear-gradient(left, red, orange);
            background: linear-gradient(to right, red, orange);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline;
            font-size: 3em;
        }
        </style>
        <div class="gradient-text">LLMs Localization</div>
        """
        
    st.markdown(gradient_text_html, unsafe_allow_html=True)
    

    st.caption(
        "A retrieval augmented generation (RAG) platform with open-source Large Language Models (LLMs) without exposing your data to online LLM providers."
    )
