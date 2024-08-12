import streamlit as st

from elements.about import about
from elements.sources import sources
from elements.settings import settings


def sidebar():
    with st.sidebar:
        tab1, tab2, tab3 = st.sidebar.tabs(["About", "Sources", "Settings"])
        with tab1:
            sources()

        with tab2:
            settings()

        with tab3:
            about()
