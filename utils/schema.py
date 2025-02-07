from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import uuid

class DocumentChunk(BaseModel):
    """Represents a single chunk of text from a document."""
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    embedding: Optional[List[float]] = None
    metadata: Dict = {}
    
class DocumentMetadata(BaseModel):
    """Metadata for a document."""
    title: Optional[str] = None
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    file_type: str
    file_size: int
    page_count: Optional[int] = None
    chunk_count: int
    source_path: str
    
class ProcessedDocument(BaseModel):
    """Complete processed document with chunks and metadata."""
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: DocumentMetadata
    chunks: List[DocumentChunk] 