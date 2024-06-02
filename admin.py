from income_report import subjects

def register_tutor(nm, lv, sj, ps):
    if lv not in range(1, 6) or sj.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]:
        return
    with open("main_database.txt", "r+") as md:
        lines = md.readlines()
        if any(nm.lower() in line for line in lines):
            return
        md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Tutor")
    with open("tutor_database.txt", "a") as td:
        td.write(f"\nTUTOR NAME: {nm.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'")

def delete_tutor(nm):
    for filename in ["main_database.txt", "tutor_database.txt"]:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            file.writelines(line for line in lines if nm.lower() not in line.lower())

def register_receptionist(nm, ps):
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Receptionist")
    with open("receptionist_database.txt", "a") as rd:
        rd.write(f"\nRECEPTIONIST NAME: {nm.title()}")

def delete_receptionist(nm):
    for filename in ["main_database.txt", "receptionist_database.txt"]:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            file.writelines(line for line in lines if nm.lower() not in line.lower())

def view_monthly_income(nm, lv, sj):
    subject_income = subjects[sj.title()]
    total_income = subject_income + lv * 1000
    print(f"{nm.title()} monthly income: RM{total_income:.2f}")

def change_profile(un, pw):
    with open("main_database.txt", "r+") as md:
        lines = md.readlines()
        md.seek(0)
        md.writelines(line for line in lines if un.lower() not in line.lower())
        md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Admin")

def register_or_delete_tutor():
    action = input("Register (type R) or Delete (type D): ").lower()
    if action == "r":
        tutor_name = input("Tutor name: ")
        tutor_level = int(input("Tutor level (1-5): "))
        tutor_subject = input("Tutor subject: ")
        tutor_password = input("Tutor temporal password (6-digits of number): ")
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
        receptionist_password = input("Receptionist temporal password (6-digits of number): ")
        register_receptionist(receptionist_name, receptionist_password)
    elif action == "d":
        receptionist_name = input("Receptionist name to delete: ")
        delete_receptionist(receptionist_name)
    else:
        print("Invalid input")

def view_income_report():
    tutor_name = input("Tutor name: ")
    tutor_level = int(input("Tutor level (1-5): "))
    tutor_subject = input("Tutor subject: ")
    view_monthly_income(tutor_name, tutor_level, tutor_subject)

def update_profile():
    admin_username = input("Admin username: ")
    admin_new_password = input("Admin new password: ")
    change_profile(admin_username, admin_new_password)

admin_message = '''
Admin functions:
1. Register/delete tutors
2. Register/delete the receptionist
3. View monthly income report of tutors
4. Update profile
'''
print(admin_message)

admin_function = int(input("Type (in number) which function to execute: "))

switch = {
    1: register_or_delete_tutor,
    2: register_or_delete_receptionist,
    3: view_income_report,
    4: update_profile
}

switch.get(admin_function, lambda: print("Invalid input"))()