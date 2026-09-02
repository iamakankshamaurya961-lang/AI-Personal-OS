import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_FILE = "backend/credentials/token.json"


def get_calendar_service():

    if not os.path.exists(TOKEN_FILE):
        raise Exception("Google account is not connected.")

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    if not credentials.valid:
        raise Exception(
            "Google credentials are invalid. Please reconnect Google Calendar."
        )

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )


from datetime import datetime, timezone


def get_calendar_events():

    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=50,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    result = []

    for event in events:

        start = event.get("start", {})

        start_datetime = start.get("dateTime")
        start_date = start.get("date")

        if start_datetime:

            event_date = start_datetime[:10]
            event_time = start_datetime[11:16]

        else:

            event_date = start_date or ""
            event_time = ""

        result.append({
            "id": event.get("id"),
            "event": event.get("summary", "No title"),
            "event_date": event_date,
            "event_time": event_time,
            "description": event.get("description", "")
        })

    print("CALENDAR EVENTS SENT TO FRONTEND:")
    print(result)

    return result

def create_calendar_event(
    title,
    start_datetime,
    end_datetime,
    description=""
):

    service = get_calendar_service()

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Asia/Kolkata"
        }
    }

    print("GOOGLE CALENDAR EVENT:")
    print(event)

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {
        "id": created_event.get("id"),
        "event": created_event.get("summary"),
        "event_date": start_datetime[:10],
        "event_time": start_datetime[11:16],
        "description": created_event.get("description", ""),
        "message": "Calendar event created successfully."
    }


def delete_calendar_event(event_id):

    service = get_calendar_service()

    print("DELETING GOOGLE EVENT ID:", event_id)

    service.events().delete(
        calendarId="primary",
        eventId=event_id
    ).execute()

    return {
        "message": "Calendar event deleted successfully."
    }