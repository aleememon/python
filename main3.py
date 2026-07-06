import gspread

# fill data in sheet using python scripts 
gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Sheets Mini Project").worksheet("Sheet2")

class UserModel:
    def __init__(self, name: str, email: str, gender: str, password: str, is_adult: bool):
        self.name = self._validate_name(name)
        self.email = self._validate_email(email)
        self.gender = self._validate_gender(gender)
        self.password = self._validate_password(password)
        self.is_adult = self._validate_is_adult(is_adult)

    def _validate_name(self, value):
        name_str = str(value).strip()
        if not name_str:
            print("Name cannot be empty or purely whitespace")
        
        return name_str
    
    def _validate_email(self, value):
        email_str = str(value).strip().lower()
        if "@" not in email_str and "." not in email_str:
            print("Invalid Email")

        return email_str

    def _validate_gender(self, value):
        gender_str = str(value).strip().lower()
        if gender_str not in ["male", "female", "other", "m", "f", "o"]:
            print("Invalid Gender")

        return gender_str  
    
    def _validate_password(self, value):
        password_str = str(value).strip()
        if len(password_str) < 8:
            print("Password must be at least 8 characters")

        has_uppercase = any(char.isupper() for char in password_str)
        has_lowercase = any(char.islower() for char in password_str)
        has_digit = any(char.isdigit() for char in password_str)
        has_special = any(char in "!@#$%^&*()_+" for char in password_str)

        if not (has_uppercase and has_lowercase and has_digit and has_special):
            print("Password must contain uppercase, lowercase, digit, and special character")

        return password_str  
    
    def _validate_is_adult(self, value):
        is_adult_str = str(value).strip().lower()
        if is_adult_str not in ["true", "false", "1", "0", "y", "n", "yes", "no"]:
            print("Invalid IsAdult value")

        return is_adult_str  

    def to_sheet_row(self):
        return [
            self.name,
            self.email,
            self.gender,
            self.password,
            self.is_adult,
        ]

def insert_user_model(user: UserModel):
    try:
        row_to_insert = user.to_sheet_row()
        sheet.append_row(row_to_insert) 
        print("User inserted successfully")
    except Exception as e:
        print(f"Error inserting user: {e}")


try: 
    user_one = UserModel("Ahmad", "ahmad@email.com", "male", "Password123@", "True")
    insert_user_model(user_one)
except Exception as e:
    print(f"Error: {e}")

    