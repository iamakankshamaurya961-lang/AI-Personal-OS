import json
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]


def get_recent_emails():

    with open("backend/credentials/token.json") as f:
        token = json.load(f)

    creds = Credentials.from_authorized_user_info(
        token,
        SCOPES
    )

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    results = service.users().messages().list(
        userId="me",
        maxResults=10
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        email = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = email["payload"]["headers"]

        subject = ""
        sender = ""
        date = ""

        for h in headers:

            if h["name"] == "Subject":
                subject = h["value"]

            elif h["name"] == "From":
                sender = h["value"]

            elif h["name"] == "Date":
                date = h["value"]

        emails.append({
            "id": email["id"],
            "subject": subject,
            "from": sender,
            "date": date,
            "snippet": email.get("snippet", "")
        })

    return emails


def get_email(email_id):

    with open("backend/credentials/token.json") as f:
        token = json.load(f)

    creds = Credentials.from_authorized_user_info(
        token,
        SCOPES
    )

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    message = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    headers = message["payload"]["headers"]

    subject = ""
    sender = ""
    date = ""

    for h in headers:

        if h["name"] == "Subject":
            subject = h["value"]

        elif h["name"] == "From":
            sender = h["value"]

        elif h["name"] == "Date":
            date = h["value"]

    body = ""

    if "parts" in message["payload"]:

        for part in message["payload"]["parts"]:

            if part["mimeType"] == "text/plain":

                if "data" in part["body"]:

                    body = base64.urlsafe_b64decode(
                        part["body"]["data"] + "=="
                    ).decode("utf-8", errors="ignore")

                    break

    elif "data" in message["payload"]["body"]:

        body = base64.urlsafe_b64decode(
            message["payload"]["body"]["data"] + "=="
        ).decode("utf-8", errors="ignore")

    return {
        "subject": subject,
        "from": sender,
        "date": date,
        "body": body
    }