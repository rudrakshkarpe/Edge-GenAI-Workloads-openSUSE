import streamlit as st

from elements.local_files import local_files
from elements.github_repo import github_repo
from elements.website import website


def sources():

    st.title("Get your data directly")
    st.caption("Convert your data into embeddings")
    st.write("")

    with st.expander("*Local Files*", expanded=False):
        local_files()

    with st.expander("*GitHub Repository*", expanded=False):
        github_repo()

    with st.expander("*Website*", expanded=False):
        website()
