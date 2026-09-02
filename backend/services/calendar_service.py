from backend.db.database import get_connection


def add_event(event, event_date, event_time):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO calendar_events
        (
            event,
            event_date,
            event_time
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,
        (
            event,
            event_date,
            event_time
        )
    )

    conn.commit()
    conn.close()


def get_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            event,
            event_date,
            event_time
        FROM calendar_events
        ORDER BY event_date,event_time
        """
    )

    rows = cursor.fetchall()

    conn.close()

    events = []

    for row in rows:

        events.append(
            {
                "id": row[0],
                "event": row[1],
                "event_date": row[2],
                "event_time": row[3]
            }
        )

    return events


def delete_event(event_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM calendar_events WHERE id=?",
        (event_id,)
    )

    conn.commit()
    conn.close()