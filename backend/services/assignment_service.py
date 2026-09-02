from backend.db.database import get_connection


def add_assignment(subject, title, deadline):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assignments
        (
            subject,
            title,
            deadline
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,
        (
            subject,
            title,
            deadline
        )
    )

    conn.commit()
    conn.close()


def get_assignments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            subject,
            title,
            deadline,
            status
        FROM assignments
        ORDER BY deadline
        """
    )

    rows = cursor.fetchall()

    conn.close()

    assignments = []

    for row in rows:

        assignments.append(
            {
                "id": row[0],
                "subject": row[1],
                "title": row[2],
                "deadline": row[3],
                "status": row[4]
            }
        )

    return assignments


def complete_assignment(assignment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE assignments
        SET status='Completed'
        WHERE id=?
        """,
        (assignment_id,)
    )

    conn.commit()
    conn.close()


def delete_assignment(assignment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assignments WHERE id=?",
        (assignment_id,)
    )

    conn.commit()
    conn.close()