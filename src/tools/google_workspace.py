import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.send'
]

class GoogleWorkspaceTool:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.authenticate()

    def authenticate(self):
        """Shows basic usage of the Gmail and Sheets API."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                # This will open a browser window for OAuth
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

    def send_email(self, to_email: str, subject: str, body: str):
        """Sends an email using the Gmail API."""
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()

            message.set_content(body)
            message['To'] = to_email
            message['Subject'] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}

            send_message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(f"Message Id: {send_message['id']}")
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def append_to_sheet(self, spreadsheet_id: str, range_name: str, values: list):
        """Appends a row of data to a Google Sheet."""
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            body = {
                'values': [values]
            }
            result = service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def get_sheet_data(self, spreadsheet_id: str, range_name: str) -> list:
        """Reads data from a Google Sheet."""
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            values = result.get('values', [])
            return values
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
