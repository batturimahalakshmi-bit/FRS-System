import csv
import os

file = "attendance.csv"

if not os.path.exists(file):
    print("No attendance records found!")
    exit()

print("\n===== ATTENDANCE RECORDS =====\n")

with open(file, "r", newline="") as f:
    reader = csv.reader(f)

    for row in reader:
        print(" | ".join(row))

print("\n==============================")