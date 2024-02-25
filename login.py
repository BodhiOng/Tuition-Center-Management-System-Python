# Import external libraries to use in this .py file
import subprocess
import sys

# Initialize attempt counter
attempt_counter = 0

# While the attempt counter is less than 3, do "this"
while attempt_counter < 3:
    # Print message and current attempt number
    print(f"---Attempt #{attempt_counter + 1}---\n(Type \"exit\" to terminate process)")

    # Prompt user for username, if user typed "exit" loop will be broken
    username = input("Enter your username: ")
    if username == "exit":
        break

    # Prompt user for password, if user typed "exit" loop will be broken
    password = input("Enter you password (6-digit numbers): ")
    if password == "exit":
        break

    # Adds 1 to the attempt counter
    attempt_counter += 1

    # Opens main_database.txt for Python to read
    with open("main_database.txt", "r") as md:
        # Read all lines in the file
        lines = md.readlines()

        # Iterate over the lines in the file
        for line in lines:
            # Check if the user-typed username and password is in the database or not
            if username.lower() in line and password in line:

                # Check if the user's status and run the respective 
                if "Admin" in line:
                    # Run the admin Python script
                    subprocess.run("python admin.py", shell=True)
                    sys.exit(0)
                # Check if the user is receptionist
                elif "Receptionist" in line:
                    # Run the receptionist Python script
                    subprocess.run("python receptionist.py", shell=True)
                    sys.exit(0)
                # Check if the user is tutor
                elif "Tutor" in line:
                    # Run the tutor Python script
                    subprocess.run("python tutor.py", shell=True)
                    sys.exit(0)
                # Check if the user is student
                elif "Student" in line:
                    # Run the student Python script
                    subprocess.run("python student.py", shell=True)
                    sys.exit(0)