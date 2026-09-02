from backend.db.database import get_connection


def add_class(day, start_time, end_time, subject, location):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO timetable
        (
            day,
            start_time,
            end_time,
            subject,
            location
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            day,
            start_time,
            end_time,
            subject,
            location
        )
    )

    conn.commit()
    conn.close()


def get_timetable():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            day,
            start_time,
            end_time,
            subject,
            location
        FROM timetable
        ORDER BY
        CASE day
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
            WHEN 'Sunday' THEN 7
        END,
        start_time
        """
    )

    rows = cursor.fetchall()

    conn.close()

    timetable = []

    for row in rows:

        timetable.append({
            "id": row[0],
            "day": row[1],
            "start_time": row[2],
            "end_time": row[3],
            "subject": row[4],
            "location": row[5]
        })

    return timetable


def delete_class(class_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM timetable WHERE id=?",
        (class_id,)
    )

    conn.commit()
    conn.close()