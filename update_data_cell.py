import gspread

gc = gspread.service_account(filename="credentials.json")
worksheet = gc.open("Sheets Mini Project").worksheet("Company Directory")

# Update cell B5 with a text string
worksheet.update_acell('B2', 'Ansar')


print("Cell updated successfully using alphanumeric notation.")
