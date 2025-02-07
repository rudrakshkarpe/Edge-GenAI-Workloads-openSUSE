import os

import streamlit as st

import utils.logs as logs

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# note: not used but required needs to be imported first
os.environ["OPENAI_API_KEY"] = "sk-abc123"

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    Document,
)

from typing import Dict, List

# setting up embeddings 


@st.cache_resource(show_spinner=False)
def setup_embedding_model(
    model: str,
):

    try:
        from torch import cuda

        device = "cpu" if not cuda.is_available() else "cuda"
    except:
        device = "cpu"
    finally:
        logs.log.info(f"Using {device} to generate embeddings")

    try:
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=model,
            device=device,
        )

        logs.log.info(f"Embedding model created successfully")

        return
    except Exception as err:
        print(f"Failed to setup the embedding model: {err}")


# load documents 


def load_documents(data_dir: str, processed_docs: List[Dict]):
    """Load documents with pre-processed chunks."""
    try:
        documents = []
        for doc in processed_docs:
            if doc["format"] == "pdf":
                for page in doc["content"]:
                    for chunk in page["chunks"]:
                        documents.append(Document(
                            text=chunk,
                            metadata={
                                "source": doc["metadata"].get("title", ""),
                                "page": page["page"],
                                "format": doc["format"]
                            }
                        ))
            else:
                for content in doc["content"]:
                    for chunk in content["chunks"]:
                        documents.append(Document(
                            text=chunk,
                            metadata={
                                "format": doc["format"],
                                "headers": content.get("structured", {}).get("headers", [])
                            }
                        ))
                        
        logs.log.info(f"Loaded {len(documents):,} chunks from documents")
        return documents
    except Exception as err:
        logs.log.error(f"Error creating data index: {err}")
        raise Exception(f"Error creating data index: {err}")

# create document index 

@st.cache_resource(show_spinner=False)
def create_index(_documents):


    try:
        index = VectorStoreIndex.from_documents(
            documents=_documents, show_progress=True
        )

        logs.log.info("Index created from loaded documents successfully")

        return index
    except Exception as err:
        logs.log.error(f"Index creation failed: {err}")
        raise Exception(f"Index creation failed: {err}")


# create query engine 

# @st.cache_resource(show_spinner=False)
def create_query_engine(_documents):
    
    try:
        index = create_index(_documents)

        query_engine = index.as_query_engine(
            similarity_top_k=st.session_state["top_k"],
            response_mode=st.session_state["chat_mode"],
            streaming=True,
        )

        st.session_state["query_engine"] = query_engine

        logs.log.info("Query Engine created successfully")

        return query_engine
    except Exception as e:
        logs.log.error(f"Error when creating Query Engine: {e}")
        raise Exception(f"Error when creating Query Engine: {e}")
