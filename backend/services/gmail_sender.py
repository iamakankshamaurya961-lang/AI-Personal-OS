import json
import base64

from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]


def send_reply(email_id, reply_body):

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

    original = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    headers = original["payload"]["headers"]

    to_email = ""
    subject = ""
    message_id = ""

    for header in headers:

        name = header["name"].lower()

        if name == "from":
            to_email = header["value"]

        elif name == "subject":
            subject = header["value"]

        elif name == "message-id":
            message_id = header["value"]

    if not to_email:
        return {
            "error": "Could not find recipient email address."
        }

    if not subject:
        subject = "Re: Your email"

    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    message = MIMEText(
        reply_body,
        "plain",
        "utf-8"
    )

    message["To"] = to_email
    message["Subject"] = subject

    if message_id:
        message["In-Reply-To"] = message_id
        message["References"] = message_id

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    send_message = {
        "raw": encoded_message,
        "threadId": original["threadId"]
    }

    sent = service.users().messages().send(
        userId="me",
        body=send_message
    ).execute()

    return {
        "success": True,
        "message": "Reply sent successfully!",
        "id": sent["id"]
    }