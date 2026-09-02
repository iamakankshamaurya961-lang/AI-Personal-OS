from backend.db.database import get_connection


def add_task(task):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(task) VALUES(?)",
        (task,)
    )

    conn.commit()
    conn.close()


def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            task,
            status
        FROM tasks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    tasks = []

    for row in rows:

        tasks.append({
            "id": row[0],
            "task": row[1],
            "status": row[2]
        })

    return tasks


def complete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()