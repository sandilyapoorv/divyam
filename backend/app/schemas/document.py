from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    doc_title: str
    page_number: int
    content: str
    score: Optional[float] = None

class DocumentMetadata(BaseModel):
    doc_id: str
    title: str
    filename: str
    total_pages: int
    total_chunks: int
    status: str

class DocumentUploadResponse(BaseModel):
    id: str
    title: str
    filename: str
    total_pages: int
    total_chunks: int
    message: str
