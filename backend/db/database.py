import sqlite3

import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

DB_NAME = os.path.join(BASE_DIR, "ai_os.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------
    # Conversation History
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        message TEXT
    )
    """)



    # --------------------------
    # Notes
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        created_at TEXT
    )
    """)

    # --------------------------
    # User Profile
    # --------------------------
    cursor.execute("""
CREATE TABLE IF NOT EXISTS profile(
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    college TEXT,
    course TEXT,
    semester TEXT,
    city TEXT,
    goals TEXT
)
""") 
    

    # --------------------------
    # Timetable
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        start_time TEXT,
        end_time TEXT,
        subject TEXT,
        location TEXT
    )
    """)

    # --------------------------
    # Assignments
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        title TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # --------------------------
    # To-Do Tasks
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # --------------------------
    # Calendar Events
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        event_date TEXT,
        event_time TEXT
    )
    """)

    # --------------------------
    # Reminders
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reminder TEXT,
        reminder_time TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    # --------------------------
    # Uploaded Documents
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        uploaded_at TEXT
    )
    """)

    conn.commit()
    conn.close()
