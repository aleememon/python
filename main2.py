import gspread

# Accessing a specific sheet (e.g: Sheet1, Sheet2...) and has names of all sheets
gc = gspread.service_account(filename="credentials.json")

spreadsheet_name = "Sheets Mini Project"
sh = gc.open(spreadsheet_name)

worksheet_name = "Sheet1"
worksheet = sh.worksheet(worksheet_name)

data = worksheet.get_all_records()
print(data)


