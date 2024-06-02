import subprocess
import sys
import os
from datetime import datetime
from peripheral_py_files.database_absolute_paths import *

attempt_counter = 0
terminated_by_user = False

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Programming-With-Python-Semester-1-Assignment"))
role_py_files_dir = os.path.join(project_dir, "role_py_files")

user_scripts = {
    "Admin": os.path.join(role_py_files_dir, "admin.py"),
    "Receptionist": os.path.join(role_py_files_dir, "receptionist.py"),
    "Tutor": os.path.join(role_py_files_dir, "tutor.py"),
    "Student": os.path.join(role_py_files_dir, "student.py")
}

def log_user(username, user_type):
    with open(databases["logged_in_users.txt"], "a") as log:
        log.write(f"{username} ({user_type}) logged in at {datetime.now()}\n")

while attempt_counter < 3:
    print(f"---Attempt #{attempt_counter + 1}---\n(Type \"exit\" to terminate process)")
    username = input("Enter your username: ").strip()
    if username == "exit":
        terminated_by_user = True
        with open(databases["logged_in_users.txt"], "w") as log:
            pass
        break
    
    password = input("Enter your password: ").strip()
    if password == "exit":
        terminated_by_user = True
        with open(databases["logged_in_users.txt"], "w") as log:
            pass
        break

    attempt_counter += 1

    with open(databases["main_database.txt"], "r") as md:
        lines = md.readlines()

        for line in lines:
            parts = line.strip().split(",")
            stored_username = parts[0].strip().lower()
            stored_password = parts[1].strip()

            if username.lower() == stored_username and password == stored_password:
                user_type = next((t for t, script in user_scripts.items() if t in line), None)

                print("both un and pw are correct")
                # if user_type:
                #     log_user(username, user_type)
                #     script_path = user_scripts[user_type]
                #     subprocess.run(["python", script_path], shell=False)
                #     sys.exit(0)
                # else:
                #     print("Invalid User Type")
                #     break
        
        print("Username or password incorrect")

if not terminated_by_user:
    print("Login Attempts Exceeded!")