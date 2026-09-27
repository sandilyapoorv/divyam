import os
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.database import get_db
from backend.app.models.document import Document
from backend.app.schemas.document import DocumentUploadResponse, DocumentMetadata
from backend.app.services.rag_engine import RagEngine

router = APIRouter(prefix="/documents", tags=["Document Ingestion"])

UPLOAD_DIR = "./backend/data/uploaded_manuals"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DocumentListItem(DocumentMetadata):
    id: str
    uploaded_at: datetime

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    doc_id = str(uuid.uuid4())
    doc_title = title or file.filename.replace("_", " ").rsplit(".", 1)[0]
    file_bytes = await file.read()

    file_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "txt"
    saved_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(saved_path, "wb") as f:
        f.write(file_bytes)

    # Ingest into RAG engine
    rag = RagEngine()
    if file_ext == "pdf":
        metadata = rag.ingest_pdf(
            pdf_bytes=file_bytes,
            doc_id=doc_id,
            title=doc_title,
            filename=file.filename
        )
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
        metadata = rag.ingest_text(
            text_pages=[text],
            doc_id=doc_id,
            title=doc_title,
            filename=file.filename
        )

    # Persist in SQL DB
    db_doc = Document(
        id=doc_id,
        title=doc_title,
        filename=file.filename,
        file_path=saved_path,
        file_type=file_ext,
        total_pages=metadata.total_pages,
        status="Indexed",
        uploaded_at=datetime.now(timezone.utc)
    )
    db.add(db_doc)
    db.commit()

    return DocumentUploadResponse(
        id=doc_id,
        title=doc_title,
        filename=file.filename,
        total_pages=metadata.total_pages,
        total_chunks=metadata.total_chunks,
        message=f"Document successfully indexed into vector database ({metadata.total_chunks} chunks)."
    )

@router.get("", response_model=List[DocumentListItem])
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [
        DocumentListItem(
            id=d.id,
            doc_id=d.id,
            title=d.title,
            filename=d.filename,
            total_pages=d.total_pages,
            total_chunks=d.total_pages * 2,
            status=d.status,
            uploaded_at=d.uploaded_at
        )
        for d in docs
    ]
