import os
import io
import uuid
import re
import hashlib
from typing import List, Optional, Dict, Any
from pypdf import PdfReader
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

from backend.app.schemas.document import DocumentChunk, DocumentMetadata
from backend.app.core.config import settings

class SimpleEmbeddingFunction(EmbeddingFunction):
    """
    Lightweight, offline vector embedding function with deterministic hashing.
    """
    def __init__(self, dim: int = 512):
        self.dim = dim

    def name(self) -> str:
        return "simple_embedding_function"

    def get_config(self) -> Dict[str, Any]:
        return {"dim": self.dim}

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = [0.0] * self.dim
            words = re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text.lower())
            if not words:
                embeddings.append(vec)
                continue
            for word in words:
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx = h % self.dim
                vec[idx] += 1.0
            norm = sum(x * x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]
            embeddings.append(vec)
        return embeddings

class RagEngine:
    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_fn = SimpleEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="mospi_documents",
            embedding_function=self.embedding_fn
        )

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> List[str]:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages.append(text)
        return pages

    def chunk_page_text(self, text: str, max_chars: int = 600, overlap: int = 100) -> List[str]:
        if not text.strip():
            return []
        
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current_chunk) + len(para) <= max_chars:
                current_chunk += ("\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk)

        if not chunks and text.strip():
            chunks = [text.strip()[:max_chars]]

        return chunks

    def ingest_text(
        self,
        text_pages: List[str],
        doc_id: str,
        title: str,
        filename: str
    ) -> DocumentMetadata:
        doc_ids = []
        documents = []
        metadatas = []
        chunk_count = 0

        for page_idx, page_content in enumerate(text_pages):
            page_num = page_idx + 1
            chunks = self.chunk_page_text(page_content)
            for chunk_idx, chunk_text in enumerate(chunks):
                chunk_id = f"{doc_id}_p{page_num}_c{chunk_idx}"
                doc_ids.append(chunk_id)
                documents.append(chunk_text)
                metadatas.append({
                    "doc_id": doc_id,
                    "doc_title": title,
                    "filename": filename,
                    "page_number": page_num,
                    "chunk_id": chunk_id
                })
                chunk_count += 1

        if documents:
            self.collection.upsert(
                ids=doc_ids,
                documents=documents,
                metadatas=metadatas
            )

        return DocumentMetadata(
            doc_id=doc_id,
            title=title,
            filename=filename,
            total_pages=len(text_pages),
            total_chunks=chunk_count,
            status="Indexed"
        )

    def ingest_pdf(
        self,
        pdf_bytes: bytes,
        doc_id: str,
        title: str,
        filename: str
    ) -> DocumentMetadata:
        pages = self.extract_text_from_pdf(pdf_bytes)
        return self.ingest_text(pages, doc_id, title, filename)

    def retrieve_relevant_chunks(
        self,
        query: str,
        doc_id: Optional[str] = None,
        top_k: int = 4
    ) -> List[DocumentChunk]:
        where_filter = {"doc_id": doc_id} if doc_id else None
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )

        chunks: List[DocumentChunk] = []
        if not results or not results.get("documents") or not results["documents"][0]:
            return chunks

        docs = results["documents"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else []
        distances = results["distances"][0] if results.get("distances") else []

        for i, text in enumerate(docs):
            meta = metas[i] if i < len(metas) else {}
            dist = distances[i] if i < len(distances) else 0.0
            chunks.append(DocumentChunk(
                chunk_id=meta.get("chunk_id", str(uuid.uuid4())),
                doc_id=meta.get("doc_id", doc_id or "unknown"),
                doc_title=meta.get("doc_title", "Official Manual"),
                page_number=int(meta.get("page_number", 1)),
                content=text,
                score=round(1.0 - float(dist), 3)
            ))

        return chunks
