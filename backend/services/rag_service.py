from backend.rag.document_loader import load_document
from backend.vectorstore.chroma_db import add_document, search_documents
import logging

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Splits text into overlapping chunks for vector storage."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_document(file_path):
    text = load_document(file_path)
    text = text.replace("\r", "")
    
    chunks = chunk_text(text)
    stored = 0
    for chunk in chunks:
        add_document(chunk)
        stored += 1
        
    logger.info(f"Stored {stored} chunks")
    return stored


def get_relevant_context(question):
    results = search_documents(question, n_results=3)
    
    if not results:
        return None
        
    logger.info("\nQUESTION:")
    logger.info(question)
    logger.info("\n========================")
    logger.info("\nRETRIEVED DOCUMENTS:\n")
    
    for i, doc in enumerate(results):
        logger.info(f"\n----- DOCUMENT {i+1} -----\n")
        logger.info(doc)
        
    logger.info("\n========================\n")
    return "\n".join(results)