from datetime import date, datetime
from backend.db.database import get_connection


def get_notifications():

    conn = get_connection()
    cursor = conn.cursor()

    notifications = []

    today = date.today()

    # ==========================================
    # ASSIGNMENTS
    # ==========================================

    cursor.execute("""
        SELECT id, subject, title, deadline, status
        FROM assignments
        WHERE status != 'Completed'
        AND deadline IS NOT NULL
    """)

    assignments = cursor.fetchall()

    for item in assignments:

        assignment_id = item[0]
        subject = item[1]
        title = item[2]
        deadline = item[3]
        status = item[4]

        try:
            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):
            continue

        days_left = (deadline_date - today).days

        if days_left < 0:

            notifications.append({
                "type": "assignment",
                "priority": "high",
                "icon": "🔴",
                "title": "Assignment overdue",
                "message": f"{title} ({subject}) is overdue.",
                "date": deadline
            })

        elif days_left == 0:

            notifications.append({
                "type": "assignment",
                "priority": "high",
                "icon": "🔴",
                "title": "Assignment due today",
                "message": f"{title} ({subject}) is due today.",
                "date": deadline
            })

        elif days_left == 1:

            notifications.append({
                "type": "assignment",
                "priority": "high",
                "icon": "🔴",
                "title": "Assignment due tomorrow",
                "message": f"{title} ({subject}) is due tomorrow.",
                "date": deadline
            })

        elif days_left <= 3:

            notifications.append({
                "type": "assignment",
                "priority": "medium",
                "icon": "🟡",
                "title": "Upcoming assignment",
                "message": f"{title} ({subject}) is due in {days_left} days.",
                "date": deadline
            })


    # ==========================================
    # PENDING TASKS
    # ==========================================

    cursor.execute("""
        SELECT id, task, status
        FROM tasks
        WHERE status != 'Completed'
    """)

    tasks = cursor.fetchall()

    for item in tasks:

        task_id = item[0]
        task = item[1]

        notifications.append({
            "type": "task",
            "priority": "low",
            "icon": "🟢",
            "title": "Pending task",
            "message": task,
            "date": None
        })


    # ==========================================
    # CALENDAR EVENTS
    # ==========================================

    cursor.execute("""
        SELECT id, event, event_date, event_time
        FROM calendar_events
        WHERE event_date IS NOT NULL
    """)

    events = cursor.fetchall()

    for item in events:

        event_id = item[0]
        event = item[1]
        event_date = item[2]
        event_time = item[3]

        try:
            event_day = datetime.strptime(
                event_date,
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):
            continue

        days_left = (event_day - today).days

        if days_left < 0:
            continue

        if days_left == 0:

            message = f"{event} is today."

            priority = "high"
            icon = "🔴"

        elif days_left == 1:

            message = f"{event} is tomorrow."

            priority = "medium"
            icon = "🟡"

        elif days_left <= 3:

            message = f"{event} is in {days_left} days."

            priority = "medium"
            icon = "🟡"

        else:

            continue

        if event_time:

            message += f" Time: {event_time}"

        notifications.append({
            "type": "calendar",
            "priority": priority,
            "icon": icon,
            "title": "Upcoming event",
            "message": message,
            "date": event_date
        })


    # ==========================================
    # REMINDERS
    # ==========================================

    cursor.execute("""
        SELECT id, reminder, reminder_time, completed
        FROM reminders
        WHERE completed = 0
    """)

    reminders = cursor.fetchall()

    for item in reminders:

        reminder_id = item[0]
        reminder = item[1]
        reminder_time = item[2]

        notifications.append({
            "type": "reminder",
            "priority": "medium",
            "icon": "🔔",
            "title": "Reminder",
            "message": reminder,
            "date": reminder_time
        })


    conn.close()

    # High priority first
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    notifications.sort(
        key=lambda x: priority_order.get(
            x["priority"],
            3
        )
    )

    return notifications