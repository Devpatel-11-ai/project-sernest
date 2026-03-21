import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

def save_contact(name, email, subject, message):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    # Goes up from core/ → sernest/ where credentials.json lives
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(BASE_DIR, 'credentials.json')
    print(f"📁 credentials path: {creds_path}")

    creds  = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    sheet  = client.open("SerNest Contact Messages").sheet1

    if not sheet.get_all_values():
        sheet.append_row(['Name', 'Email', 'Subject', 'Message', 'Date'])

    date = datetime.now().strftime('%d-%m-%Y %H:%M')
    sheet.append_row([name, email, subject, message, date])
    print("✅ Saved to Google Sheet!")