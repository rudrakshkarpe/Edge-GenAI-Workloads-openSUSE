import streamlit as st


def set_page_config():
    st.set_page_config(
        page_title="LLMs Localization",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state=st.session_state["sidebar_state"],
        menu_items={
           "Get Help":"https://github.com/rudrakshkarpe/Edge-GenAI-Workloads-openSUSE/",
        })

    # Remove the Streamlit `Deploy` button from the Header
    st.markdown(
        r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
