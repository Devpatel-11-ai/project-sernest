import gspread
from google.oauth2.service_account import Credentials
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_contact(name, email, subject, message):

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        os.path.join(BASE_DIR, "sernest-26dd7a1ce791.json"),
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("SerNest Contact Messages").sheet1

    sheet.append_row([name, email, subject, message])