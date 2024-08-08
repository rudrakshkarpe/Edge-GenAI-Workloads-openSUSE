import streamlit as st


def set_page_header():
    st.set_page_config(
        page_title="🏠 Localization of LLMs",
        page_icon="🏠",
        layout="centered",
        initial_sidebar_state=st.session_state["sidebar_state"],
        menu_items={
            "Discussions": "https://github.com/rudrakshkarpe/Edge-GenAI-Workloads-openSUSE/issues"
        },
    )


st.markdown(
    r"""
    
    <style>
    .stDeployButton{
        visibility: hidden;
    }
    </style>
    """,
    
    unsafe_allow_html=True,
    
)