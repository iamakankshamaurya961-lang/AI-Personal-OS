import os
import pdfplumber
from docx import Document


def load_document(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)
    elif extension == ".docx":
        return load_docx(file_path)
    elif extension == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError("Unsupported file type")


def load_pdf(path):
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


def load_docx(path):
    doc = Document(path)
    text_chunks = []
    for para in doc.paragraphs:
        text_chunks.append(para.text)
    return "\n".join(text_chunks)


def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()