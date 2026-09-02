from datetime import datetime


def create_note_object(content):
    return {
        "content": content,
        "created_at": datetime.now().isoformat()
    }