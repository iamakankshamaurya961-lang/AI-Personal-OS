import logging
from datetime import date, datetime
from backend.db.database import get_connection

logger = logging.getLogger(__name__)


def get_notifications():
    """Aggregates notifications from assignments, tasks, calendar, and reminders."""
    conn = get_connection()
    notifications = []
    today = date.today()

    try:
        cursor = conn.cursor()

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
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
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

    finally:
        conn.close()

    # --- CALENDAR: Fetch from Google Calendar ---
    try:
        from backend.calendar.calender_manager import get_calendar_events
        events = get_calendar_events()
        for event in events:
            event_date_str = event.get("date", "")
            try:
                event_day = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            days_left = (event_day - today).days
            if days_left < 0:
                continue
            if days_left == 0:
                priority = "high"
                message = f"📅 Today: {event.get('title', 'Event')} at {event.get('time', 'N/A')}"
            elif days_left <= 2:
                priority = "medium"
                message = f"📅 In {days_left} day(s): {event.get('title', 'Event')}"
            else:
                continue
            notifications.append({
                "type": "calendar",
                "message": message,
                "priority": priority,
            })
    except Exception:
        logger.warning("Could not fetch Google Calendar events for notifications")

    # High priority first
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    notifications.sort(
        key=lambda x: priority_order.get(x["priority"], 3)
    )

    return notifications
