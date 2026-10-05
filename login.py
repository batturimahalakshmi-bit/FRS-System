import tkinter as tk
from tkinter import messagebox
import subprocess
import sys


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Login Successful", "Welcome to FRS!")
        root.destroy()

        subprocess.Popen(
            [sys.executable, "attendance_gui.py"]
        )

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password"
        )


# Main window
root = tk.Tk()

root.title("FRS Login")
root.geometry("400x300")


# Title
title = tk.Label(
    root,
    text="Face Recognition System",
    font=("Arial", 20, "bold")
)

title.pack(pady=25)


# Username
username_label = tk.Label(
    root,
    text="Username",
    font=("Arial", 12)
)

username_label.pack()

username_entry = tk.Entry(
    root,
    font=("Arial", 12)
)

username_entry.pack(pady=5)


# Password
password_label = tk.Label(
    root,
    text="Password",
    font=("Arial", 12)
)

password_label.pack()

password_entry = tk.Entry(
    root,
    show="*",
    font=("Arial", 12)
)

password_entry.pack(pady=5)


# Login button
login_button = tk.Button(
    root,
    text="Login",
    command=login,
    font=("Arial", 12, "bold"),
    padx=30,
    pady=8
)

login_button.pack(pady=20)


root.mainloop()