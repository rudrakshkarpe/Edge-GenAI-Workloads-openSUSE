import streamlit as st 

from tabs.about import about 
from tabs.sources import sources
from tabs.settings import settings


def sidebar():
    with st.sidebar:
        tab1, tab2, tab3 = st.sidebar.tabs(["About", "Sources", "Settings"])
        
        with tab1:
            sources()
            
        with tab2:
            settings()
            
        with tab3:
            about()
    