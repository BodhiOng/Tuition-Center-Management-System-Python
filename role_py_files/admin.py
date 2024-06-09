import random
import string
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from peripheral_py_files.income_report import subjects
from peripheral_py_files.user_messages import admin_message, subjects_list
from peripheral_py_files.database_absolute_paths import databases

def main():
    def register_tutor(nm, lv, sj, ps):
        if lv not in range(1, 6):
            print(f"Invalid level: {lv}. Level must be between 1 and 5.")
            return
        
        if sj.title() not in subjects:
            print(f"Invalid subject: {sj}. Subject not found in the subjects list.")
            return
        
        try:
            with open(databases["main_database.txt"], "r+") as md:
                lines = md.readlines()
                if any(nm.lower() in line for line in lines):
                    print("The tutor already exists in the database.")
                    return
                md.write(f"USERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Tutor\n")

            with open(databases["tutor_database.txt"], "a") as td:
                td.write(f"TUTOR NAME: {nm.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'\n")
            print("Tutor successfully added to the database.")
        except Exception as e:
            print(f"An error occurred while registering the tutor: {e}")

    def delete_tutor(nm):
        try:
            for filename in [databases["main_database.txt"], databases["tutor_database.txt"]]:
                with open(filename, "r") as file:
                    lines = file.readlines()

                with open(filename, "w") as file:
                    file.writelines(line for line in lines if nm.lower() not in line.lower())

            print("Tutor successfully deleted from the database.")
        except Exception as e:
            print(f"An error occurred while deleting the tutor: {e}")

    def register_receptionist(nm, ps):
        try:
            with open(databases["main_database.txt"], "a") as md:
                md.write(f"USERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Receptionist\n")

            with open(databases["receptionist_database.txt"], "a") as rd:
                rd.write(f"RECEPTIONIST NAME: {nm.title()}\n")

            print("Receptionist successfully added to the database.")
        except Exception as e:
            print(f"An error occurred while registering the receptionist: {e}")

    def delete_receptionist(nm):
        try:
            for filename in [databases["main_database.txt"], databases["receptionist_database.txt"]]:
                with open(filename, "r") as file:
                    lines = file.readlines()

                with open(filename, "w") as file:
                    file.writelines(line for line in lines if nm.lower() not in line.lower())

            print("Receptionist successfully deleted from the database.")
        except Exception as e:
            print(f"An error occurred while deleting the receptionist: {e}")

    def view_monthly_income(nm):
        try:
            with open(databases["tutor_database.txt"], "r") as td:
                lines = td.readlines()
                for line in lines:  
                    if nm in line:
                        sj = line.split("SUBJECT: '")[1].split("'")[0]
                        lv = int(line.split("LEVEL: Form ")[1].split(", SUBJECT:")[0])
                        break
                else:
                    print(f"Tutor {nm.title()} not found in the database.")
                    return
            subject_income = subjects.get(sj.title(), 0)
            total_income = subject_income + lv * 1000

            print(f"{nm.title()} monthly income: RM{total_income:.2f}")
        except Exception as e:
            print(f"An error occurred while viewing the monthly income: {e}")

    def change_profile(un, pw):
        try:
            with open(databases["main_database.txt"], "r+") as md:
                lines = md.readlines()
                md.seek(0)
                md.truncate()
                md.writelines(line for line in lines if un.lower().strip() not in line.lower().strip())
                md.write(f"USERNAME: {un.lower().strip()}, PASSWORD: {pw}, STATUS: Admin\n")

            print("Profile updated successfully.")
        except Exception as e:
            print(f"An error occurred while changing the profile: {e}")

    digits = string.digits

    def register_or_delete_tutor():
        action = input("Register (type R) or Delete (type D): ").lower()
        if action == "r":
            tutor_name = input("Tutor name: ")
            tutor_level = int(input("Tutor level (1-5): "))
            print(subjects_list)
            tutor_subject = input("Tutor subject: ")
            tutor_password = ''.join(random.choice(digits) for i in range(6))

            register_tutor(tutor_name, tutor_level, tutor_subject, tutor_password)
        elif action == "d":
            tutor_name = input("Tutor name to delete: ")

            delete_tutor(tutor_name)
        else:
            print("Invalid input")

    def register_or_delete_receptionist():
        action = input("Register (type R) or Delete (type D): ").lower()
        if action == "r":
            receptionist_name = input("Receptionist name: ")
            receptionist_password = ''.join(random.choice(digits) for i in range(6))

            register_receptionist(receptionist_name, receptionist_password)
        elif action == "d":
            receptionist_name = input("Receptionist name to delete: ")

            delete_receptionist(receptionist_name)
        else:
            print("Invalid input")

    def view_income_report():
        tutor_name = input("Tutor name: ").title()

        view_monthly_income(tutor_name)

    def update_profile():
        try:
            username = ""
            with open(databases["logged_in_users.txt"], "r") as liu: 
                lines = liu.readlines()
                for line in lines:
                    if "(" in line:
                        username = line[0:line.index("(")]
                        break

            if not username:
                print("No valid logged in user found.")
                return
            
            old_password = input("Re-enter your old password to verify: ")
            valid_user = False

            with open(databases["main_database.txt"], "r") as md: 
                lines = md.readlines()
                for line in lines:
                    if username in line and old_password in line:
                        valid_user = True
                        break

            if not valid_user:
                print("Invalid username or password.")
                return
            
            new_password = input("Enter your new password: ")

            change_profile(username, new_password)
        except Exception as e:
            print(f"An error occurred while updating the profile: {e}")

    def quit_program():
        try:
            with open(databases["logged_in_users.txt"], "w") as file:
                file.truncate(0)

            print("Exiting program....")
            sys.exit()
        except Exception as e:
            print(f"An error occurred while quitting the program: {e}")

    while True:
        print(admin_message)
        try:
            admin_function = int(input("Type (in number) which function to execute: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        switch = {
            1: register_or_delete_tutor,
            2: register_or_delete_receptionist,
            3: view_income_report,
            4: update_profile,
            5: quit_program
        }

        func = switch.get(admin_function, lambda: print("Invalid input"))
        func()

        pass