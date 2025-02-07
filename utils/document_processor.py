import fitz  # PyMuPDF
import markdown
import bs4
import docx
import json
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path
import os

class DocumentProcessor:
    """Handles document parsing and preprocessing before embedding."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.supported_formats = {
            '.pdf': self._process_pdf,
            '.md': self._process_markdown,
            '.txt': self._process_text,
            '.docx': self._process_docx
        }
    
    def _process_pdf(self, file_path: str) -> Dict:
        """Extract text and metadata from PDF files."""
        try:
            doc = fitz.open(file_path)
            content = []
            metadata = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "total_pages": len(doc),
                "page_content": {}
            }
            
            for page_num, page in enumerate(doc):
                # Extract text
                page_text = page.get_text()
                
                # Create chunks for this page
                text_chunks = self.chunk_text(page_text)
                chunks = []
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "metadata": {"page": page_num}
                    })
                
                metadata["page_content"][page_num] = {
                    "text_length": len(page_text),
                    "chunk_count": len(chunks)
                }
                
                content.append({
                    "page": page_num,
                    "chunks": chunks
                })
            
            return {
                "content": content,
                "metadata": metadata,
                "format": "pdf"
            }
            
        except Exception as e:
            logging.error(f"Error processing PDF file {file_path}: {str(e)}")
            return None
    
    def _extract_pdf_images(self, page) -> List[Dict]:
        """Extract images from PDF page."""
        images = []
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            if base_image:
                images.append({
                    "index": img_index,
                    "data": base_image["image"],
                    "extension": base_image["ext"]
                })
        return images
    
    def _process_markdown(self, file_path: str) -> Dict:
        """Process markdown files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
            
        # Convert to HTML for better structure parsing
        html = markdown.markdown(md_text)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        # Extract structured content
        headers = [h.text for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [p.text for p in soup.find_all('p')]
        
        return {
            "content": [{
                "text": md_text,
                "structured": {
                    "headers": headers,
                    "paragraphs": paragraphs
                }
            }],
            "metadata": {
                "headers_count": len(headers),
                "paragraphs_count": len(paragraphs)
            },
            "format": "markdown"
        }
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        if not text.strip():
            return []
        
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1  # +1 for space
            
            if current_size >= self.chunk_size:
                chunks.append(" ".join(current_chunk))
                # Move back by overlap
                overlap_words = current_chunk[-self.chunk_overlap:]
                current_chunk = overlap_words
                current_size = sum(len(word) + 1 for word in overlap_words)
        
        # Add the last chunk if it exists and isn't too small
        if current_chunk and current_size > self.chunk_size / 4:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def _process_text(self, file_path: str) -> Dict:
        """Process plain text files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Split text into chunks
            chunks = []
            words = text.split()
            current_chunk = []
            current_size = 0
            
            for word in words:
                current_chunk.append(word)
                current_size += len(word) + 1  # +1 for space
                
                if current_size >= self.chunk_size:
                    chunks.append({
                        "text": " ".join(current_chunk),
                        "metadata": {}
                    })
                    current_chunk = []
                    current_size = 0
            
            if current_chunk:  # Add the last chunk if it exists
                chunks.append({
                    "text": " ".join(current_chunk),
                    "metadata": {}
                })
            
            return {
                "content": [{
                    "page": 0,  # Single page for text files
                    "chunks": chunks
                }],
                "metadata": {
                    "title": os.path.basename(file_path),
                    "author": None,
                    "total_chars": len(text)
                },
                "format": "txt"
            }
        except Exception as e:
            logging.error(f"Error processing text file {file_path}: {str(e)}")
            return None
    
    def _process_docx(self, file_path: str) -> Dict:
        """Process Microsoft Word (.docx) files."""
        try:
            doc = docx.Document(file_path)
            
            # Extract text from paragraphs
            full_text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Skip empty paragraphs
                    full_text.append(paragraph.text)
            
            # Join all text with newlines
            text = '\n'.join(full_text)
            
            # Get document properties
            properties = doc.core_properties
            
            return {
                "content": [{
                    "text": text,
                    "chunks": self.chunk_text(text)
                }],
                "metadata": {
                    "title": properties.title or os.path.basename(file_path),
                    "author": properties.author,
                    "created_at": properties.created,
                    "modified_at": properties.modified,
                    "total_paragraphs": len(doc.paragraphs),
                    "total_chars": len(text)
                },
                "format": "docx"
            }
        except Exception as e:
            logging.error(f"Error processing DOCX file {file_path}: {str(e)}")
            return None
    
    def process_document(self, file_path: str) -> Optional[Dict]:
        """Main method to process any supported document."""
        try:
            file_ext = Path(file_path).suffix.lower()
            if file_ext in self.supported_formats:
                processor = self.supported_formats[file_ext]
                result = processor(file_path)
                
                # Chunk the content
                if result["format"] == "pdf":
                    for page in result["content"]:
                        page["chunks"] = self.chunk_text(page["text"])
                else:
                    for content in result["content"]:
                        content["chunks"] = self.chunk_text(content["text"])
                
                return result
            else:
                logging.error(f"Unsupported file format: {file_ext}")
                return None
                
        except Exception as e:
            logging.error(f"Error processing document {file_path}: {str(e)}")
            return None 