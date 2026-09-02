from backend.db.database import get_connection


def get_profile():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM profile WHERE id=1"
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return {
            "name": "",
            "email": "",
            "phone": "",
            "college": "",
            "course": "",
            "semester": "",
            "city": "",
            "goals": ""
        }

    return {

        "name": row[1],
        "email": row[2],
        "phone": row[3],
        "college": row[4],
        "course": row[5],
        "semester": row[6],
        "city": row[7],
        "goals": row[8]

    }


def save_profile(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO profile

    (id,name,email,phone,college,course,semester,city,goals)

    VALUES

    (1,?,?,?,?,?,?,?,?)

    """, (

        data["name"],
        data["email"],
        data["phone"],
        data["college"],
        data["course"],
        data["semester"],
        data["city"],
        data["goals"]

    ))

    conn.commit()
    conn.close()