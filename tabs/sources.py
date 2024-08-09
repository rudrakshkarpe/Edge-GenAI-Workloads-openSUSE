import streamlit as st

from tabs.local_files import local_files

def sources():
    
    st.title("Get your data directly")
    st.caption("Convert your data into embeddings")
    st.write("")    
    
    with st.expander("*Local Files*",
                     expanded=False):
        local_files()

        
        
        

        
        
    

