import gspread

gc = gspread.service_account(filename="credentials.json")
sh = gc.open("Sheets Mini Project")
worksheet = sh.worksheet("Sheet2")

# This completely clears all cells but keeps the grid cells empty
worksheet.clear()
print("All cell data has been cleared.")
