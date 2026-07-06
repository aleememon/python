import gspread

# Delete a row
gc = gspread.service_account(filename="credentials.json")
sheet = gc.open("Sheets Mini Project").worksheet("Sheet2")



try:
    row_to_delete = 2
    # deleting specifying rows
    # sheet.delete_rows(start_index, end_index)
    sheet.delete_rows(row_to_delete)    
    print("Row deleted successfully")
except gspread.exceptions.APIError:
    print(f"Error: {row_to_delete} is not a valid row number")