import subprocess
import sys
import os
import importlib
from datetime import datetime
from peripheral_py_files.database_absolute_paths import databases

attempt_counter = 0
terminated_by_user = False

user_scripts = {
    "Admin": "role_py_files.admin",
    "Receptionist": "role_py_files.receptionist",
    "Tutor": "role_py_files.tutor",
    "Student": "role_py_files.student"
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
            if username.lower() in line and password in line:
                user_type = next((t for t, script in user_scripts.items() if t in line), None)

                if user_type:
                    log_user(username, user_type)
                    module_name = user_scripts[user_type]
                    role_module = importlib.import_module(module_name)
                    role_module.main()
                    sys.exit(0)
                else:
                    print("Invalid User Type")
                    break
        
        print("Username or password incorrect")

if not terminated_by_user:
    print("Login Attempts Exceeded!")