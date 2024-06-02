import subprocess
import sys
from datetime import datetime

attempt_counter = 0

user_scripts = {
    "Admin": "admin.py",
    "Receptionist": "receptionist.py",
    "Tutor": "tutor.py",
    "Student": "student.py"
}

def log_user(username, user_type):
    with open("logged_in_users.txt", "a") as log:
        log.write(f"{username} ({user_type}) logged in at {datetime.now()}\n")

while attempt_counter < 3:
    print(f"---Attempt #{attempt_counter + 1}---\n(Type \"exit\" to terminate process)")
    username = input("Enter your username: ")
    if username == "exit":
        break
    
    password = input("Enter you password (6-digit numbers): ")
    if password == "exit":
        break

    attempt_counter += 1

    with open("main_database.txt", "r") as md:
        lines = md.readlines()

        for line in lines:
            if username.lower() in line and password in line:
                user_type = next((t for t, script in user_scripts.items() if t in line), None)
                if user_type:
                    log_user(username, user_type)
                    subprocess.run(["python", user_scripts[user_type]], shell=False)
                    sys.exit(0)
                else:
                    print("Invalid User Type")
                    break
        else:
            print("Username or password in correct")

print("Login Attempts Exceeded!")