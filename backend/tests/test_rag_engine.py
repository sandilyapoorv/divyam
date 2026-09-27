import pytest
import io
from pypdf import PdfWriter

def test_rag_document_ingestion_and_retrieval(tmp_path):
    from backend.app.services.rag_engine import RagEngine
    from backend.app.schemas.document import DocumentChunk

    # Create a small realistic multi-page test PDF in memory
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    
    # We will test with sample text content via the text ingestion path
    sample_text_page1 = (
        "Ministry of Statistics and Programme Implementation (MoSPI).\n"
        "Chapter 1: Consumer Price Index (CPI) Methodology.\n"
        "The Consumer Price Index measures changes over time in the general level of prices of goods and services "
        "that a reference population acquires, uses or pays for. The current base year is 2012=100. "
        "Price relatives are aggregated at the primary subgroup level using the Geometric Mean (Jevons Index)."
    )
    sample_text_page2 = (
        "Chapter 2: Periodic Labour Force Survey (PLFS) Rotational Sampling.\n"
        "In urban areas, a rotational panel sampling design is used where each selected sample household is visited "
        "four times in consecutive quarters. This ensures 75% sample overlap between consecutive quarters to estimate "
        "changes in Current Weekly Status (CWS) and Labour Force Participation Rate (LFPR)."
    )

    rag = RagEngine(persist_dir=str(tmp_path / "chroma_test"))

    # Ingest text document
    doc_id = "test-doc-001"
    metadata = rag.ingest_text(
        text_pages=[sample_text_page1, sample_text_page2],
        doc_id=doc_id,
        title="MoSPI Statistical Guidelines Handbook 2024",
        filename="mospi_guidelines.txt"
    )

    assert metadata.total_chunks >= 2
    assert metadata.doc_id == doc_id

    # 1. Query for CPI base year and geometric mean
    cpi_chunks = rag.retrieve_relevant_chunks("What is the base year and formula for Consumer Price Index?", doc_id=doc_id, top_k=2)
    assert len(cpi_chunks) > 0
    assert any("2012=100" in c.content for c in cpi_chunks)
    assert any("Geometric Mean" in c.content for c in cpi_chunks)
    # Check page attribution
    assert cpi_chunks[0].page_number == 1
    assert cpi_chunks[0].doc_title == "MoSPI Statistical Guidelines Handbook 2024"

    # 2. Query for PLFS rotational panel
    plfs_chunks = rag.retrieve_relevant_chunks("How many visits are conducted in urban PLFS rotational panel?", doc_id=doc_id, top_k=2)
    assert len(plfs_chunks) > 0
    assert any("four times" in c.content for c in plfs_chunks)
    assert plfs_chunks[0].page_number == 2
