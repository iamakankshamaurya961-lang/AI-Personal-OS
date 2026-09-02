from backend.services.email_ai import (
    summarize_email,
    generate_email_reply
)
from backend.services.gmail_reader import (
    get_recent_emails,
    get_email
)


from backend.services.gmail_reader import get_email



from backend.services.gmail_service import get_google_flow, send_reply
from fastapi.responses import RedirectResponse
from backend.services.profile_service import (
    get_profile,
    save_profile
)
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware


import os
import sqlite3
import re
from backend.db.database import init_db
from backend.db.database import get_connection
from backend.services.memory_service import (
    save_message,
    load_messages,
    load_notes,
    save_note,
)

from backend.services.context_builder import build_prompt

from backend.services.ai_service import (
    ask_llama,
    should_save_memory,
)

from backend.services.rag_service import ingest_document

from backend.vectorstore.chroma_db import clear_documents

from backend.services.profile_service import (
    save_profile,
    get_profile,
)

from backend.services.timetable_service import (
    add_class,
    get_timetable,
    delete_class,
)

from backend.services.assignment_service import (
    add_assignment,
    get_assignments,
    complete_assignment,
    delete_assignment,
)
from backend.services.task_service import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
)
from backend.calender.calender_manager import (
    get_calendar_events,
    create_calendar_event,
    delete_calendar_event
)
from backend.services.notification_service import get_notifications
oauth_data = {}
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/")
def home():
    return {
        "message": "AI Personal OS Backend is running!"
    }


# ======================================
# PROFILE
# ======================================

@app.get("/profile")
def profile():
    return get_profile()




# ======================================
# TIMETABLE
# ======================================

@app.get("/timetable")
def timetable():
    return get_timetable()


@app.post("/timetable")
def create_class(data: dict):

    add_class(
        data.get("day", ""),
        data.get("start_time", ""),
        data.get("end_time", ""),
        data.get("subject", ""),
        data.get("location", "")
    )

    return {
        "message": "Class added successfully."
    }


@app.delete("/timetable/{class_id}")
def remove_class(class_id: int):

    delete_class(class_id)

    return {
        "message": "Class deleted successfully."
    }


# ======================================
# ASSIGNMENTS
# ======================================

@app.get("/assignments")
def assignments():
    return get_assignments()


@app.post("/assignments")
def create_assignment(data: dict):

    add_assignment(
        data.get("subject", ""),
        data.get("title", ""),
        data.get("deadline", "")
    )

    return {
        "message": "Assignment added successfully."
    }


@app.put("/assignments/{assignment_id}")
def finish_assignment(assignment_id: int):

    complete_assignment(assignment_id)

    return {
        "message": "Assignment marked as completed."
    }


@app.delete("/assignments/{assignment_id}")
def remove_assignment(assignment_id: int):

    delete_assignment(assignment_id)

    return {
        "message": "Assignment deleted successfully."
    }

# ======================================
# TASKS
# ======================================

@app.get("/tasks")
def tasks():
    return get_tasks()


@app.post("/tasks")
def create_task(data: dict):

    add_task(
        data.get("task", "")
    )

    return {
        "message": "Task added successfully."
    }


@app.put("/tasks/{task_id}")
def finish_task(task_id: int):

    complete_task(task_id)

    return {
        "message": "Task marked as completed."
    }


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):

    delete_task(task_id)

    return {
        "message": "Task deleted successfully."
    }
# ======================================
# CALENDAR
# ======================================
@app.get("/calendar")
def calendar():
    return get_calendar_events()


@app.post("/calendar")
def create_event(data: dict):

    print("RECEIVED FROM FRONTEND:")
    print(data)

    event_date = data.get("event_date")
    event_time = data.get("event_time")

    if not event_date or not event_time:
        return {
            "message": "Date and time are required."
        }

    start_datetime = f"{event_date}T{event_time}:00+05:30"

    from datetime import datetime, timedelta

    start = datetime.fromisoformat(start_datetime)

    end = start + timedelta(hours=1)

    end_datetime = end.isoformat()

    print("START:", start_datetime)
    print("END:", end_datetime)

    event = create_calendar_event(
        data.get("event", ""),
        start_datetime,
        end_datetime,
        data.get("description", "")
    )

    return event


@app.delete("/calendar/{event_id}")
def remove_event(event_id: str):
    return delete_calendar_event(event_id)

# ======================================
# NOTES
# ======================================

@app.get("/notes")
def get_notes():

    notes = load_notes()

    return {
        "notes": notes
    }

@app.get("/memory")
def get_memory():

    notes = load_notes()

    return {
        "memory": notes
    }


@app.post("/profile")
async def update_profile(profile: dict):

    save_profile(profile)

    return {
        "message": "Profile Saved Successfully"
    }
# ======================================
# CHAT
# ======================================



# ==============================
# TASK COMMANDS
# ==============================



@app.get("/ask")
def ask(question: str):

    question_clean = question.strip()

    # ==============================
    # ADD TASK
    # ==============================

    add_match = re.match(
        r"^(?:add|create)\s+(?:a\s+)?task(?:\s+to)?\s+(.+)$",
        question_clean,
        re.IGNORECASE
    )

    if add_match:

        task_name = add_match.group(1).strip()

        if not task_name:
            return {
                "answer": "Please provide a task name."
            }

        add_task(task_name)

        return {
            "answer": f'Task "{task_name}" added successfully.'
        }

    # ==============================
    # COMPLETE TASK
    # ==============================

    complete_match = re.match(
        r"^(?:complete|finish)\s+task\s+(\d+)$",
        question_clean,
        re.IGNORECASE
    )

    if complete_match:

        task_id = int(complete_match.group(1))

        complete_task(task_id)

        return {
            "answer": f"Task {task_id} marked as completed."
        }

    # ==============================
    # DELETE TASK
    # ==============================

    delete_match = re.match(
        r"^(?:delete|remove)\s+task\s+(\d+)$",
        question_clean,
        re.IGNORECASE
    )

    if delete_match:

        task_id = int(delete_match.group(1))

        delete_task(task_id)

        return {
            "answer": f"Task {task_id} deleted successfully."
        }

    # ==============================
    # NORMAL AI CHAT
    # ==============================

    if should_save_memory(question):

        save_note(question)

    notes = load_notes()

    tasks = get_tasks()

    save_message("user", question)

    history = load_messages(limit=30)

    prompt = build_prompt(
        notes,
        history,
        question,
        tasks
    )

    data = ask_llama(prompt)

    if "response" in data:

        ai_answer = data["response"]

        save_message(
            "assistant",
            ai_answer
        )

        return {
            "answer": ai_answer
        }

    return {
        "error": data,
        "message": "Ollama did not return expected response"
    }
# DOCUMENT UPLOAD
# ======================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    os.makedirs("backend/uploads", exist_ok=True)

    file_path = f"backend/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    clear_documents()

    chunks = ingest_document(file_path)

    return {
        "message": f"{file.filename} uploaded successfully.",
        "chunks": chunks
    }
# ======================================
# DASHBOARD
# ======================================

@app.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM assignments WHERE status='Pending'")
    assignments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'")
    tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notes")
    memories = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM timetable")
    classes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM calendar_events")
    events = cursor.fetchone()[0]

    cursor.execute("SELECT name FROM profile WHERE id=1")
    row = cursor.fetchone()

    name = row[0] if row else "User"

    conn.close()

    return {
        "name": name,
        "assignments": assignments,
        "tasks": tasks,
        "memories": memories,
        "classes": classes,
        "events": events
    }
@app.delete("/clear_chat")
def clear_chat():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages")

    conn.commit()
    conn.close()

    return {
        "message":"Chat cleared successfully!"
    }
@app.get("/auth/login")
def gmail_login():

    flow = get_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    oauth_data["state"] = state
    oauth_data["code_verifier"] = flow.code_verifier

    return RedirectResponse(authorization_url)
from fastapi import Request
import os






@app.get("/auth/callback")
def gmail_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None
):

    # ==============================
    # GOOGLE AUTH ERROR
    # ==============================

    if error:

        return {
            "error": "Google authorization was not completed.",
            "details": error
        }

    # ==============================
    # VERIFY STATE
    # ==============================

    if state != oauth_data.get("state"):

        return {
            "error": "Invalid OAuth state."
        }

    # ==============================
    # CHECK CODE
    # ==============================

    if not code:

        return {
            "error": "Authorization code was not received."
        }

    # ==============================
    # RESTORE GOOGLE FLOW
    # ==============================

    flow = get_google_flow()

    flow.code_verifier = oauth_data.get("code_verifier")

    # ==============================
    # EXCHANGE CODE FOR TOKEN
    # ==============================

    try:

        flow.fetch_token(code=code)

    except Exception as e:

        return {
            "error": "Failed to connect Google account.",
            "details": str(e)
        }

    credentials = flow.credentials

    # ==============================
    # SAVE TOKEN
    # ==============================

    os.makedirs(
        "backend/credentials",
        exist_ok=True
    )

    with open(
        "backend/credentials/token.json",
        "w"
    ) as token:

        token.write(
            credentials.to_json()
        )

    return {
        "message": "Google account connected successfully!"
    }
@app.get("/gmail")
def gmail():
    return get_recent_emails()
@app.get("/gmail/{email_id}")
def gmail_email(email_id: str):
    return get_email(email_id)
@app.post("/gmail/reply")
def gmail_reply(data: dict):

    body = data.get("body", "")

    if not body:
        return {
            "error": "Email body is empty"
        }

    reply = generate_email_reply(body)

    return {
        "reply": reply
    }
@app.post("/gmail/send-reply")
def gmail_send_reply(data: dict):

    email_id = data.get("email_id", "")
    body = data.get("body", "")

    if not email_id:
        return {
            "error": "Email ID is missing."
        }

    if not body:
        return {
            "error": "Reply body is empty."
        }

    try:

        result = send_reply(
            email_id,
            body
        )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/gmail/summarize")
def gmail_summary(data: dict):

    body = data.get("body", "")

    if not body:
        return {
            "error": "Email body is empty"
        }

    summary = summarize_email(body)

    return {
        "summary": summary
    }
@app.get("/notifications")
def notifications():

    return get_notifications()
@app.get("/search")
def global_search(query: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    results = []

    cursor.execute(
        "SELECT subject,title,deadline FROM assignments"
    )

    for row in cursor.fetchall():

        text = (
            row["subject"] + " " +
            row["title"] + " " +
            row["deadline"]
        ).lower()

        if query.lower() in text:

            results.append({
                "type":"Assignment",
                "title":row["title"],
                "subtitle":row["subject"]
            })

    cursor.execute(
        "SELECT task,status FROM tasks"
    )

    for row in cursor.fetchall():

        text = (
            row["task"] + " " +
            row["status"]
        ).lower()

        if query.lower() in text:

            results.append({
                "type":"Task",
                "title":row["task"],
                "subtitle":row["status"]
            })

    cursor.execute(
        "SELECT event,event_date FROM calendar_events"
    )

    for row in cursor.fetchall():

        text = (
            row["event"] + " " +
            row["event_date"]
        ).lower()

        if query.lower() in text:

            results.append({
                "type":"Event",
                "title":row["event"],
                "subtitle":row["event_date"]
            })

    cursor.execute(
        "SELECT subject,day,start_time FROM timetable"
    )

    for row in cursor.fetchall():

        text = (
            row["subject"] + " " +
            row["day"] + " " +
            row["start_time"]
        ).lower()

        if query.lower() in text:

            results.append({
                "type":"Class",
                "title":row["subject"],
                "subtitle":row["day"]
            })

    conn.close()

    return results
