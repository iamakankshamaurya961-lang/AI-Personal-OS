from pypdf import PdfReader
from docx import Document
import os


def load_document(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension == ".txt":
        return load_txt(file_path)

    else:
        raise Exception("Unsupported file type")


import pdfplumber


import pdfplumber

def load_pdf(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def load_docx(path):
    doc = Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def load_txt(path):

    with open(path, "r", encoding="utf-8") as f:
        return f.read()