import time 

import streamlit as st 

from pages.chatbox import chatbox

import pages.chatbox import chatbox
import pages.header import set_page_header
import pages.sidebar import sidebar
import pages.page_config import set_page_config
import pages.page_state import set_initial_state



def welcome_message(msg: str):
    
    for char in msg:
        time.sleep(0.20) # Sleep for 250 milliseconds

    st.markdown(f"<h1 style='text-align: center; color: #000000;'>{msg}</h1>", unsafe_allow_html=True)


    yield char
    
set_initial_state()

set_page_config()
set_page_header()


for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])
    
sidebar()


chatbox()


