from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]


def get_google_flow():

    flow = Flow.from_client_secrets_file(
        "backend/credentials/client_secret.json",
        scopes=SCOPES
    )

    flow.redirect_uri = "http://localhost:8000/auth/callback"

    return flow


def send_reply(email_id, body):

    token_path = "backend/credentials/token.json"

    if not os.path.exists(token_path):
        raise Exception("Google account is not connected.")

    credentials = Credentials.from_authorized_user_file(
        token_path,
        SCOPES
    )

    if not credentials.valid:

        if credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request

            credentials.refresh(Request())

            with open(token_path, "w") as token:
                token.write(credentials.to_json())

        else:
            raise Exception(
                "Google authentication expired. Please reconnect Gmail."
            )

    gmail = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    original = gmail.users().messages().get(
        userId="me",
        id=email_id,
        format="metadata",
        metadataHeaders=[
            "From",
            "To",
            "Subject",
            "Message-ID"
        ]
    ).execute()

    headers = {
        header["name"].lower(): header["value"]
        for header in original.get("payload", {}).get("headers", [])
    }

    to = headers.get("from")

    subject = headers.get("subject", "")

    message_id = headers.get("message-id")

    if not to:
        raise Exception("Could not determine original sender.")

    reply_subject = subject

    if not reply_subject.lower().startswith("re:"):
        reply_subject = "Re: " + reply_subject

    message = MIMEText(body)

    message["To"] = to
    message["Subject"] = reply_subject

    if message_id:
        message["In-Reply-To"] = message_id
        message["References"] = message_id

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    sent = gmail.users().messages().send(
        userId="me",
        body={
            "raw": raw_message,
            "threadId": email_id
        }
    ).execute()

    return {
        "message": "Reply sent successfully.",
        "id": sent.get("id")
    }