import gspread

gc = gspread.service_account(filename="credentials.json")
worksheet = gc.open("Sheets Mini Project").worksheet("Company Directory")

data_matrix = [
    ["6", "Ali Raza", "IT"],
    ["7", "Saif Ali", "Finance"],
    ["8", "Irfan", "Supply Chain"],
    ["9", "Hassan", "HR"],
    ["10", "Bilal", "Marketing"]
]

worksheet.update(range_name='A2:C6', values=data_matrix)

print("Range A2:C6 successfully updated with data matrix.")
