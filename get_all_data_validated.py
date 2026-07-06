import gspread
from dataclasses import dataclass
from typing import List

@dataclass
class Employee:
    id: str
    name: str
    department: str

gc = gspread.service_account(filename="credentials.json")
sheet = gc.open("Sheets Mini Project").worksheet("Company Directory")

raw_records = sheet.get_all_records()
employee_list: List[Employee] =  [
    Employee(
        id=row["id"], 
        name=row["name"], 
        department=row["department"]
        )
    for row in raw_records
]

for employee in employee_list:
    print(f"ID: {employee.id} | Name: {employee.name} | Department: {employee.department}")