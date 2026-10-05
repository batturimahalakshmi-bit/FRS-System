import tkinter as tk
from tkinter import ttk
import csv
import os
import subprocess
import sys
from datetime import datetime


def get_statistics():

    total_students = 0
    present_students = set()
    total_records = 0

    # Count registered students
    if os.path.exists("known_faces"):

        total_students = len([
            f for f in os.listdir("known_faces")
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])

    # Count attendance
    if os.path.exists("attendance.csv"):

        with open("attendance.csv", "r", newline="") as f:

            reader = csv.reader(f)
            next(reader, None)

            for row in reader:

                if len(row) >= 3:

                    total_records += 1

                    today = datetime.now().strftime("%d-%m-%Y")

                    if row[1] == today:
                        present_students.add(row[0])

    present_today = len(present_students)

    return total_students, present_today, total_records


def update_statistics():

    total, present, records = get_statistics()

    total_label.config(text=str(total))
    present_label.config(text=str(present))
    records_label.config(text=str(records))


def load_attendance():

    # Clear old table data
    for item in table.get_children():
        table.delete(item)

    if not os.path.exists("attendance.csv"):
        update_statistics()
        return

    with open("attendance.csv", "r", newline="") as f:

        reader = csv.reader(f)

        # Skip header
        next(reader, None)

        for row in reader:

            if len(row) >= 3:

                table.insert(
                    "",
                    "end",
                    values=(row[0], row[1], row[2])
                )

    update_statistics()


def start_face_recognition():

    subprocess.Popen(
        [sys.executable, "face_recognition.py"]
    )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Face Recognition Attendance System")
root.geometry("800x600")


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="Face Recognition Attendance System",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


# ==========================================
# STATISTICS FRAME
# ==========================================

stats_frame = tk.Frame(root)

stats_frame.pack(pady=10)


# ==========================================
# TOTAL STUDENTS
# ==========================================

total_box = tk.Frame(
    stats_frame,
    bd=2,
    relief="groove",
    padx=35,
    pady=15
)

total_box.grid(
    row=0,
    column=0,
    padx=10
)


tk.Label(
    total_box,
    text="Total Students",
    font=("Arial", 12, "bold")
).pack()


total_label = tk.Label(
    total_box,
    text="0",
    font=("Arial", 20, "bold")
)

total_label.pack()


# ==========================================
# PRESENT TODAY
# ==========================================

present_box = tk.Frame(
    stats_frame,
    bd=2,
    relief="groove",
    padx=35,
    pady=15
)

present_box.grid(
    row=0,
    column=1,
    padx=10
)


tk.Label(
    present_box,
    text="Present Today",
    font=("Arial", 12, "bold")
).pack()


present_label = tk.Label(
    present_box,
    text="0",
    font=("Arial", 20, "bold")
)

present_label.pack()


# ==========================================
# TOTAL RECORDS
# ==========================================

records_box = tk.Frame(
    stats_frame,
    bd=2,
    relief="groove",
    padx=35,
    pady=15
)

records_box.grid(
    row=0,
    column=2,
    padx=10
)


tk.Label(
    records_box,
    text="Total Records",
    font=("Arial", 12, "bold")
).pack()


records_label = tk.Label(
    records_box,
    text="0",
    font=("Arial", 20, "bold")
)

records_label.pack()


# ==========================================
# START FACE RECOGNITION BUTTON
# ==========================================

start_button = tk.Button(
    root,
    text="Start Face Recognition",
    command=start_face_recognition,
    font=("Arial", 13, "bold"),
    padx=20,
    pady=10
)

start_button.pack(pady=15)


# ==========================================
# ATTENDANCE TABLE
# ==========================================

columns = (
    "Name",
    "Date",
    "Time"
)


table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=10
)


table.heading(
    "Name",
    text="Name"
)

table.heading(
    "Date",
    text="Date"
)

table.heading(
    "Time",
    text="Time"
)


table.column(
    "Name",
    width=200
)

table.column(
    "Date",
    width=200
)

table.column(
    "Time",
    width=200
)


table.pack(pady=10)


# ==========================================
# REFRESH BUTTON
# ==========================================

refresh_button = tk.Button(
    root,
    text="Refresh Attendance",
    command=load_attendance,
    font=("Arial", 12)
)

refresh_button.pack(pady=10)


# ==========================================
# LOAD DATA
# ==========================================

load_attendance()


# ==========================================
# START GUI
# ==========================================

root.mainloop()