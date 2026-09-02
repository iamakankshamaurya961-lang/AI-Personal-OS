from backend.db.database import get_connection
from backend.vectorstore.chroma_db import (
    add_document,
    search_documents
)


def save_message(role, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages(role, message) VALUES (?, ?)",
        (role, message)
    )

    conn.commit()
    conn.close()


def load_messages(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM messages
        ORDER BY id ASC
        LIMIT ?
        """,
        (limit,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


def load_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM notes"
    )

    notes = cursor.fetchall()

    conn.close()

    return notes


def save_note(content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes(content, created_at)
        VALUES (?, datetime('now'))
        """,
        (content,)
    )

    conn.commit()
    conn.close()

    # Store in vector database
    add_document(content)


def search_notes(query):
    return search_documents(query)