import chromadb
from sentence_transformers import SentenceTransformer
import re

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def clear_documents():
    global collection

    try:
        client.delete_collection("documents")
    except:
        pass

    collection = client.get_or_create_collection(
        name="documents"
    )


def add_document(text):

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(collection.count() + 1)],
        documents=[text],
        embeddings=[embedding]
    )


def add_memory(text):
    add_document(text)


def search_memory(query):
    return search_documents(query)


def search_documents(query, n_results=10):

    # ---------- Detect semester ----------
    semester = None

    match = re.search(
        r"semester\s*([ivx0-9]+)",
        query,
        re.IGNORECASE
    )

    if match:
        semester = match.group(1).upper()

    # ---------- If asking semester, return exact semester ----------
    if semester:

        docs = collection.get()["documents"]

        exact = []

        for doc in docs:

            if f"SEMESTER -{semester}" in doc.upper():
                exact.append(doc)

        if exact:
            return exact

    # ---------- Semantic Search ----------
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["documents", "distances"]
    )

    # No documents
    if len(results["documents"][0]) == 0:
        return []

    # Distance of best match
    distance = results["distances"][0][0]

    print("Distance:", distance)

    # Ignore unrelated matches
    if distance > 1.2:
        return []

    return results["documents"][0]