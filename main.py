from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import string

class User:
    def __init__(self, name, email, password, gender, is_adult, sign_in):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.is_adult = is_adult
        self.sign_in = sign_in
    
    def __repr__(self):
        return f"User: Name={self.name}, Email={self.email}, Gender={self.gender}, IsAdult={self.is_adult} SignIn={self.sign_in}"


def validate_name(name):
    return isinstance(name, str) and len(name.strip()) >= 2


def validate_email(email):
    email = email.strip()
    return "@" in email


def validate_password(password):
    if not isinstance(password, str) or len(password.strip()) < 8:
        return False
    
    has_special = any(char in string.punctuation for char in password)
    has_numbers = any(char in string.digits for char in password)
    has_upper = any(char in string.ascii_uppercase for char in password)
    has_lower = any(char in string.ascii_lowercase for char in password)
        
    return has_special and has_numbers and has_upper and has_lower


def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        val_clean = value.strip().lower()
        if val_clean in ('true', 'yes', 'y', '1', 'checked', 'x'):
            return True
        return False
    return False


def fetch_and_process_sheet_data():
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except FileNotFoundError:
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found in current directory")
        print("Please download your Google Service Account credentials and save as 'credentials.json'")
        return []
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return []
    
    SPREADSHEET_ID = '168JLfcfvws4oERACmnQijgUc29c1vgc_NLS-ONnW408'
    RANGE_NAME = 'Sheet1!A2:F'
    
    import re
    if not isinstance(SPREADSHEET_ID, str) or not re.match(r'^[a-zA-Z0-9-_]{30,100}$', SPREADSHEET_ID):
        print("Error: Invalid Spreadsheet ID format.")
        return []
        
    if not isinstance(RANGE_NAME, str) or "!" not in RANGE_NAME or not RANGE_NAME.strip():
        print("Error: Invalid Range format. Expected 'SheetName!Range'.")
        return []
    
    try:
        print("Connecting to Google Sheets...")
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

        raw_rows = result.get('values', [])

        if not raw_rows:
            print("No data found in the spreadsheet.")
            return []
        
        return process_rows(raw_rows)

    except HttpError as e:
        print(f"HTTP Error: {e.resp.status} - {e.content.decode()}")
        return []
    except Exception as err:
        error_msg = str(err)
        if "oauth2.googleapis.com" in error_msg or "Unable to find the server" in error_msg:
            print("Network Error: Cannot reach Google servers")
            print("Possible causes:")
            print("  - No internet connection")
            print("  - Firewall/Proxy blocking googleapis.com")
            print("  - DNS resolution issues")
            print("\nTo test locally without internet, run: python main.py --mock")
            return []
        else:
            print(f"Error: {err}")
            return []

def process_rows(raw_rows):
    valid_users = []
    errors = []

    for index, row in enumerate(raw_rows):
        row_num = index + 2
        
        while len(row) < 6:
            row.append("")

        name = row[0].strip()
        email = row[1].strip()
        password = row[2].strip()
        gender = row[3].strip()
        is_adult = parse_boolean(row[4].strip())
        sign_in = row[5].strip()

        all_valid = True
        error_messages = []

        if not validate_name(name):
            all_valid = False
            error_messages.append("Name must be at least 2 characters")
        
        if not validate_email(email):
            all_valid = False
            error_messages.append("Email must contain @ and .")
        
        if not validate_password(password):
            all_valid = False
            error_messages.append("Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters")

        if all_valid:
            user = User(name, email, password, gender, is_adult, sign_in)
            valid_users.append(user)
        else:
            errors.append({
                "row": row_num,
                "errors": error_messages
            })

    print(f"\nSuccessfully processed {len(valid_users)} users:")
    for user in valid_users:
        print(f"  - {user}")
    
    if errors:
        print(f"\nEncountered errors in {len(errors)} rows:")
        for error in errors:
            print(f"Row {error['row']}: {', '.join(error['errors'])}")

    return valid_users


fetch_and_process_sheet_data()