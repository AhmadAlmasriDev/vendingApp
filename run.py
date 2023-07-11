import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json') 
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
MACHINES_SHEET = GSPREAD_CLIENT.open('VendingMachine')
SALES_SHEET = GSPREAD_CLIENT.open('VendingSales')
ALARM_SHEET = GSPREAD_CLIENT.open('Alarms')

machines = MACHINES_SHEET.worksheet('Template')

data = machines.get_all_values()
print(data)