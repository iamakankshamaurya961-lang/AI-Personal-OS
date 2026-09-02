from backend.rag.document_loader import load_document
from backend.vectorstore.chroma_db import add_document, search_documents
import re


def ingest_document(file_path):

    text = load_document(file_path)

    # Normalize spaces
    text = text.replace("\r", "")

    # Find every semester heading
    pattern = r"SEMESTER\s*-\s*(I|II|III|IV|V|VI|VII|VIII)"

    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))

    stored = 0

    for i in range(len(matches)):

        start = matches[i].start()

        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(text)

        chunk = text[start:end].strip()

        # Remove detailed syllabus pages if they exist
        stop_words = [
            "DETAILED SYLLABI",
            "DETAILED SYLLABI",
            "Syllabus:",
            "MATHEMATICS I 3-1-0-4",
            "MATHEMATICS II 3-1-0-4"
        ]

        cut = len(chunk)

        for word in stop_words:
            pos = chunk.find(word)
            if pos != -1:
                cut = min(cut, pos)

        chunk = chunk[:cut].strip()

        if len(chunk) > 100:
            add_document(chunk)
            stored += 1

    print(f"Stored {stored} semester chunks")

    return stored


def get_relevant_context(question):

    results = search_documents(question, n_results=1)

    if not results:
        return "No relevant document found."

    print("\nQUESTION:")
    print(question)

    print("\n========================")
    print("\nRETRIEVED DOCUMENTS:\n")

    context = ""

    for i, doc in enumerate(results):

        print(f"\n----- DOCUMENT {i+1} -----\n")
        print(doc)

        context += doc + "\n"

    print("\n========================\n")

    return context