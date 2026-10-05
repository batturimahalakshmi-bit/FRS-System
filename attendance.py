import csv
from datetime import datetime
import os

name = "Maha"

file = "attendance.csv"

file_exists = os.path.exists(file)

with open(file, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["Name", "Date", "Time"])

    now = datetime.now()

    writer.writerow([
        name,
        now.strftime("%d-%m-%Y"),
        now.strftime("%H:%M:%S")
    ])

print("Attendance marked successfully!")