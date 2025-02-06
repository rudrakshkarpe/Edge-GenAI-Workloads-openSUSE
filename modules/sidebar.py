import streamlit as st

from components.about import about
from components.sources import sources
from components.settings import settings

def sidebar():
    with st.sidebar:
        tab1, tab2, tab3 = st.sidebar.tabs(["Files", "Models", "About"])
        with tab1:
            sources()

        with tab2:
            settings()

        with tab3:
            about()
