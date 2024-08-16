import os
import sys
import shutil
import inspect

import streamlit as st

import utils.helpers as func
import utils.ollama as ollama
import utils.llama_index as llama_index
import utils.logs as logs


def rag_pipeline(uploaded_files: list = None):
    
    error = None

    # saving files to disk (optional)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                save_dir = os.getcwd() + "/data"
                func.save_uploaded_file(uploaded_file, save_dir)

        st.caption("✔️ Files Uploaded")
    
    # create llama index service context to use local embeddings 

    try:
        llm = ollama.create_ollama_llm(
            st.session_state["selected_model"],
            st.session_state["ollama_endpoint"],
            st.session_state["system_prompt"],
        )
        st.session_state["llm"] = llm
        st.caption("✔️ LLM Initialized")

    except Exception as err:
        logs.log.error(f"Failed to setup LLM: {str(err)}")
        error = err
        st.exception(error)
        st.stop()

    # choose the embedding model

    embedding_model = st.session_state["embedding_model"]
    hf_embedding_model = None

    if embedding_model == None:
        hf_embedding_model = "BAAI/bge-large-en-v1.5"

    if embedding_model == "Default (bge-large-en-v1.5)":
        hf_embedding_model = "BAAI/bge-large-en-v1.5"

    # if embedding_model == "Large (Salesforce/SFR-Embedding-Mistral)":
    #     hf_embedding_model = "Salesforce/SFR-Embedding-Mistral"

    if embedding_model == "Other":
        hf_embedding_model = st.session_state["other_embedding_model"]

    try:
        llama_index.setup_embedding_model(
            hf_embedding_model,
        )
        st.caption("✔️ Embedding Model Created")
    except Exception as err:
        logs.log.error(f"Setting up Embedding Model failed: {str(err)}")
        error = err
        st.exception(error)
        st.stop()
    
    # choose files from local dir

    if (
        st.session_state["documents"] is not None
        and len(st.session_state["documents"]) > 0
    ):
        logs.log.info("Documents are already available; skipping document loading")
        st.caption("✔️ Processed File Data")
    else:
        try:
            save_dir = os.getcwd() + "/data"
            documents = llama_index.load_documents(save_dir)
            st.session_state["documents"] = documents
            st.caption("✔️ Data Processed")
        except Exception as err:
            logs.log.error(f"Document Load Error: {str(err)}")
            error = err
            st.exception(error)
            st.stop()
    
    # create index from ingest documents 

    try:
        llama_index.create_query_engine(
            st.session_state["documents"],
        )
        st.caption("✔️ Created File Index")
    except Exception as err:
        logs.log.error(f"Index Creation Error: {str(err)}")
        error = err
        st.exception(error)
        st.stop()

    
    # remove files from data 
    
    if len(st.session_state["file_list"]) > 0:
        try:
            save_dir = os.getcwd() + "/data"
            shutil.rmtree(save_dir)
            st.caption("✔️ Removed Temp Files")
        except Exception as err:
            logs.log.warning(
                f"Unable to delete data files, you may want to clean-up manually: {str(err)}"
            )
            pass

    return error  # If no errors occurred, None is returned
