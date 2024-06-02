import random
import string
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from peripheral_py_files.income_report import *
from peripheral_py_files.user_messages import *
from peripheral_py_files.database_absolute_paths import *

digits = string.digits

def register_tutor(nm, lv, sj, ps):
    if lv not in range(1, 6) or sj.title() not in subjects:
        return
    with open(databases["main_database.txt"], "r+") as md:
        lines = md.readlines()
        if any(nm.lower() in line for line in lines):
            print("The tutor had already existed in the database")
            return
        md.write(f"USERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Tutor\n")
    with open(databases["tutor_database.txt"], "a") as td:
        td.write(f"TUTOR NAME: {nm.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'\n")

    print("Tutor successfully added to the database")

def delete_tutor(nm):
    for filename in [databases["main_database.txt"], databases["tutor_database.txt"]]:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            file.writelines(line for line in lines if nm.lower() not in line.lower())

    print("Tutor successfully deleted from the database")

def register_receptionist(nm, ps):
    with open(databases["main_database.txt"], "a") as md:
        md.write(f"USERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Receptionist\n")
    with open(databases["receptionist_database.txt"], "a") as rd:
        rd.write(f"RECEPTIONIST NAME: {nm.title()}\n")

    print("Receptionist successfully added to the database")

def delete_receptionist(nm):
    for filename in [databases["main_database.txt"], databases["receptionist_database.txt"]]:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            file.writelines(line for line in lines if nm.lower() not in line.lower())

    print("Receptionist successfully deleted from the database")

def view_monthly_income(nm):
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

def change_profile(un, pw):
    with open(databases["main_database.txt"], "r+") as md:
        lines = md.readlines()
        md.seek(0)
        md.writelines(line for line in lines if un.lower() not in line.lower())
        md.write(f"USERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Admin\n")

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
    admin_new_password = input(f"Re-enter your old password to verify: ")
    # change_profile(admin_username, admin_new_password)

print(admin_message)
admin_function = int(input("Type (in number) which function to execute: "))

switch = {
    1: register_or_delete_tutor,
    2: register_or_delete_receptionist,
    3: view_income_report,
    4: update_profile
}

switch.get(admin_function, lambda: print("Invalid input"))()