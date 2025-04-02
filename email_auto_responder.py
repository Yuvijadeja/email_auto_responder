import os
import base64
import openai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def fetch_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data['payload']
        headers = payload.get("headers", [])
        subject = sender = ""
        for header in headers:
            if header["name"] == "From":
                sender = header["value"]
            if header["name"] == "Subject":
                subject = header["value"]
        body = ""
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode()
        emails.append((msg['id'], sender, subject, body))
    return emails

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def send_email(service, recipient, subject, body):
    message = MIMEText(body)
    message["to"] = recipient
    message["subject"] = "Re: " + subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

if __name__ == "__main__":
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    emails = fetch_unread_emails(service)
    print(emails)
    for msg_id, sender, subject, body in emails:
        response_text = generate_response(body)
        send_email(service, sender, subject, response_text)
        service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        print(f"Replied to {sender} with AI-generated response.")
