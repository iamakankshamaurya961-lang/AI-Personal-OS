from backend.services.rag_service import get_relevant_context


def build_prompt(notes, history, question, tasks):

    relevant_context = get_relevant_context(question)

    conversation = ""

    for role, message in history[-10:]:
        if role == "user":
            conversation += f"User: {message}\n"
        else:
            conversation += f"Assistant: {message}\n"

    task_text = ""

    if tasks:
        for task in tasks:
            status = task.get("status", "Pending")
            task_name = task.get("task", "")

            task_text += f"- {task_name} [{status}]\n"
    else:
        task_text = "No tasks found."

    # ---------------- NORMAL CHAT ----------------

    if (
        relevant_context == ""
        or relevant_context == "No relevant document found."
    ):

        return f"""
You are a helpful, intelligent AI assistant.

You are part of the user's Personal OS.

IMPORTANT:
- Answer the latest user question directly.
- Do not invent tasks.
- When the user asks about their tasks, use the REAL TASK LIST below.
- Do not say that you do not have information about the user's tasks if the task list contains them.
- Do not generate fake tasks.
- Do not generate fake "User:" messages.

REAL TASK LIST:
{task_text}

Conversation History:
{conversation}

Latest User Question:
{question}

Your Answer:
"""

    # ---------------- DOCUMENT CHAT ----------------

    return f"""
You are a helpful AI assistant.

You are part of the user's Personal OS.

Use the uploaded document ONLY if it helps answer the question.

If the document is unrelated, ignore it completely.

REAL TASK LIST:
{task_text}

Document:
{relevant_context}

Conversation History:
{conversation}

Latest User Question:
{question}

Your Answer:
"""