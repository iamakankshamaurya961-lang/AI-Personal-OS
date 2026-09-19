import chromadb
from sentence_transformers import SentenceTransformer
import uuid
import logging

logger = logging.getLogger(__name__)

client = chromadb.PersistentClient(path="chroma_db")

doc_collection = client.get_or_create_collection(name="documents")
mem_collection = client.get_or_create_collection(name="memories")

model = SentenceTransformer("all-MiniLM-L6-v2")


def clear_documents():
    """Clears only the documents collection, preserving user memories."""
    global doc_collection
    try:
        client.delete_collection(name="documents")
    except Exception:
        pass
    doc_collection = client.get_or_create_collection(name="documents")


def add_document(text):
    embedding = model.encode(text).tolist()
    doc_collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
        embeddings=[embedding]
    )


def add_memory(text):
    embedding = model.encode(text).tolist()
    mem_collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
        embeddings=[embedding]
    )


def search_memory(query):
    embedding = model.encode(query).tolist()
    results = mem_collection.query(
        query_embeddings=[embedding],
        n_results=10,
        include=["documents", "distances"]
    )
    if not results or not results.get("documents") or len(results["documents"][0]) == 0:
        return []
    distance = results["distances"][0][0]
    logger.info("Distance: %s", distance)
    if distance > 1.2:
        return []
    return results["documents"][0]


def search_documents(query, n_results=10):
    embedding = model.encode(query).tolist()
    results = doc_collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["documents", "distances"]
    )
    if not results or not results.get("documents") or len(results["documents"][0]) == 0:
        return []
    distance = results["distances"][0][0]
    logger.info("Distance: %s", distance)
    if distance > 1.2:
        return []
    return results["documents"][0]