import streamlit as st 

import utils.rag_pipeline as rag


from llama_index.readers.web import SimpleWebPageReader
from urllib.parse import urlparse


def ensure_https(url: str) -> str:
    parsed = urlparse(url)
    
    if not bool(parsed.scheme):
        return f"https://{url}"
    return url

def website():

    st.write("Enter the URL of website")
    col1, col2 = st.columns([1, 0.2])

    with col1:
        new_website = st.text_input("Website URL",
        label_visibility = "collapsed")

    with col2:
        add_buttom = st.button("➕")

    if add_buttom and new_website != "":
        st.session_state["websites"].append(ensure_https(new_website))
        st.session_state["websites"] = sorted(set(st.session_state["websites"]))

    if st.session_state["websites"]:
        st.markdown(f"<p>Website(s)</p>", unsafe_allow_html=True)
        for site in st.session_state["websites"]:
            st.caption(f"- {site}")
        st.write("")

        process_button = st.button("Process", key="process_website")

        if process_button:
            document = SimpleWebPageReader(html_to_text=True).load_data(st.session_state["websites"])

            if len(document) > 0:
                st.session_state["documents"] = document

                with st.spinner("Processing..."):
                    # rag pipeline intitiation and storing document in the disk if needed
                    error = rag.rag_pipeline()

                    if error is not None:
                        st.exception(error)
                    else:
                        st.write(
                            "Website processing completed, Let's get to the chat!🚀"
                        )
