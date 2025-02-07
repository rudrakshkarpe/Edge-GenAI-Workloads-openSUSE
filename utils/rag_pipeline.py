import os
import sys
import shutil
import inspect
from typing import List, Dict

import streamlit as st
from sentence_transformers import SentenceTransformer

import utils.helpers as func
import utils.ollama as ollama
import utils.llama_index as llama_index
import utils.logs as logs
from utils.document_processor import DocumentProcessor
from utils.vector_store import VectorStore
from utils.schema import ProcessedDocument, DocumentMetadata, DocumentChunk

def initialize_embedding_model():
    """Initialize the embedding model."""
    if "embedding_model" not in st.session_state:
        try:
            # Using a default model, you can make this configurable
            model_name = "all-MiniLM-L6-v2"
            st.session_state["embedding_model"] = SentenceTransformer(model_name)
            logs.log.info(f"Initialized embedding model: {model_name}")
        except Exception as e:
            logs.log.error(f"Error initializing embedding model: {e}")
            raise

def create_embedding(text: str) -> List[float]:
    """Create embedding using the configured model."""
    if "embedding_model" not in st.session_state:
        initialize_embedding_model()
    return st.session_state["embedding_model"].encode(text).tolist()

def rag_pipeline(uploaded_files: list = None):
    """Enhanced RAG pipeline with vector storage."""
    try:
        # Initialize components
        initialize_embedding_model()  # Initialize embedding model first
        processor = DocumentProcessor(
            chunk_size=st.session_state.get("chunk_size", 1024),
            chunk_overlap=st.session_state.get("chunk_overlap", 200)
        )
        vector_store = VectorStore()
        
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Save file temporarily
                    save_dir = os.path.join(os.getcwd(), "data")
                    temp_path = os.path.join(save_dir, uploaded_file.name)
                    os.makedirs(save_dir, exist_ok=True)
                    
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process document
                    doc_result = processor.process_document(temp_path)
                    
                    if doc_result:
                        # Create embeddings for chunks
                        for content in doc_result["content"]:
                            for chunk in content["chunks"]:
                                chunk["embedding"] = create_embedding(chunk["text"])
                        
                        # Convert to Pydantic model
                        processed_doc = ProcessedDocument(
                            metadata=DocumentMetadata(
                                title=doc_result["metadata"].get("title"),
                                author=doc_result["metadata"].get("author"),
                                file_type=doc_result["format"],
                                file_size=os.path.getsize(temp_path),
                                page_count=len(doc_result["content"]),
                                chunk_count=sum(len(c["chunks"]) for c in doc_result["content"]),
                                source_path=uploaded_file.name
                            ),
                            chunks=[
                                DocumentChunk(
                                    text=chunk["text"],
                                    embedding=chunk["embedding"],
                                    metadata={"page": content.get("page")}
                                )
                                for content in doc_result["content"]
                                for chunk in content["chunks"]
                            ]
                        )
                        
                        # Store in vector database
                        vector_store.store_document(processed_doc)
                    
                    # Cleanup
                    os.remove(temp_path)
                    
            st.caption("✔️ Files Processed and Indexed")
        
        return None
        
    except Exception as err:
        logs.log.error(f"RAG Pipeline Error: {str(err)}")
        return err

def process_documents(uploaded_files: list) -> List[Dict]:
    """Process uploaded documents through the digitization pipeline."""
    processor = DocumentProcessor(
        chunk_size=st.session_state.get("chunk_size", 1024),
        chunk_overlap=st.session_state.get("chunk_overlap", 200)
    )
    
    processed_docs = []
    for file in uploaded_files:
        save_path = os.path.join(os.getcwd(), "data", file.name)
        
        # Save file temporarily
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        
        # Process the document
        result = processor.process_document(save_path)
        if result:
            processed_docs.append(result)
            
        # Clean up
        os.remove(save_path)
        
    return processed_docs
