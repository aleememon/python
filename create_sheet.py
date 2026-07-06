import gspread

gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Sheets Mini Project")

new_sheet = sheet.add_worksheet(title="July Expenses", rows=100, cols=10)

print(f"new sheet created title:{new_sheet.title}")

