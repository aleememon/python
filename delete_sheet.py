
import gspread
import gspread
gc = gspread.service_account(filename="credentials.json")
sheet = gc.open("Sheets Mini Project")
to_delete_sheet_name = "July Expenses"
try:
    worksheet_obj = sheet.worksheet(to_delete_sheet_name)

    sheet.del_worksheet(worksheet_obj)

    print(f"Delete sheet: {to_delete_sheet_name} successfully")
except gspread.exceptions.WorksheetNotFound:
    print(f"Error: {to_delete_sheet_name} not found in the spreadsheet")

