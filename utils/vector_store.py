import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from typing import List, Dict, Optional
import os
from utils.schema import ProcessedDocument, DocumentChunk
import logging
from dotenv import load_dotenv

class VectorStore:
    def __init__(self, connection_string: Optional[str] = None):
        load_dotenv()
        self.conn_string = connection_string or os.getenv('DATABASE_URL')
        if not self.conn_string:
            raise ValueError("Database connection string not provided")
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database with required tables and extensions."""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                # Enable vector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Create documents table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        doc_id TEXT PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        created_at TIMESTAMP WITH TIME ZONE,
                        file_type TEXT,
                        file_size INTEGER,
                        page_count INTEGER,
                        chunk_count INTEGER,
                        source_path TEXT
                    );
                """)
                
                # Create chunks table with vector support
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chunks (
                        chunk_id TEXT PRIMARY KEY,
                        doc_id TEXT REFERENCES documents(doc_id),
                        text TEXT,
                        embedding vector(1536),
                        metadata JSONB,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create vector index
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS chunks_embedding_idx 
                    ON chunks 
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                """)
                
                conn.commit()
    
    def store_document(self, processed_doc: ProcessedDocument):
        """Store a processed document and its chunks."""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                # Store document metadata
                cur.execute("""
                    INSERT INTO documents 
                    (doc_id, title, author, created_at, file_type, file_size, 
                     page_count, chunk_count, source_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    processed_doc.doc_id,
                    processed_doc.metadata.title,
                    processed_doc.metadata.author,
                    processed_doc.metadata.created_at,
                    processed_doc.metadata.file_type,
                    processed_doc.metadata.file_size,
                    processed_doc.metadata.page_count,
                    processed_doc.metadata.chunk_count,
                    processed_doc.metadata.source_path
                ))
                
                # Store chunks with embeddings
                chunk_data = [(
                    chunk.chunk_id,
                    processed_doc.doc_id,
                    chunk.text,
                    chunk.embedding,
                    chunk.metadata
                ) for chunk in processed_doc.chunks]
                
                execute_values(cur, """
                    INSERT INTO chunks (chunk_id, doc_id, text, embedding, metadata)
                    VALUES %s
                """, chunk_data)
                
                conn.commit()
    
    def semantic_search(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Perform semantic search using vector similarity."""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.chunk_id, c.text, c.metadata, d.title,
                           1 - (c.embedding <=> %s) as similarity
                    FROM chunks c
                    JOIN documents d ON c.doc_id = d.doc_id
                    ORDER BY c.embedding <=> %s
                    LIMIT %s;
                """, (query_embedding, query_embedding, limit))
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'chunk_id': row[0],
                        'text': row[1],
                        'metadata': row[2],
                        'document_title': row[3],
                        'similarity_score': row[4]
                    })
                
                return results 