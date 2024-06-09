import string
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from peripheral_py_files.income_report import subjects
from peripheral_py_files.user_messages import receptionist_message
from peripheral_py_files.database_absolute_paths import databases
from peripheral_py_files.user_messages import *

def main():
    def register_student_func(nm, ps, sjs, sd_i):
        valid_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        sjs = [sub.title() for sub in sjs]

        for sub in sjs:
            if sub not in subjects:
                print(f"Invalid subject: {sub}. Subject not found in the subjects list.")
                return

        if sd_i[5].title() not in valid_months or not 1 <= int(sd_i[4]) <= 5:
            print("Invalid month or level.")
            return
        
        with open(databases["main_database.txt"], "r") as md_check:
            lines = md_check.readlines()
            for line in lines:
                if nm.lower() in line.lower():
                    print("Student already exists.")
                    return

        with open(databases["main_database.txt"], "a") as md:
            md.write(f"USERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Student\n")

        with open(databases["student_database.txt"], "a") as sd:
            sd.write(f"STUDENT NAME: {nm.title()}, LEVEL: Form {sd_i[4]}, SUBJECT(S): {', '.join(sjs)}, IC/PASSPORT: {sd_i[0]}, EMAIL: {sd_i[1]}, CONTACT NUMBER: {sd_i[2]}, ADDRESS: {sd_i[3]}, MONTH OF ENROLLMENT: {sd_i[5].title()}\n")

        with open(databases["payment_status.txt"], "a") as ps:
            ps.write(f"STUDENT NAME: {nm.title()}, PAYMENT STATUS: Unpaid\n")

    def update_subject_enrollment(nm, n_sjs):
        with open(databases["student_database.txt"], "r") as sd:
            lines = sd.readlines()

        updated_lines = []
        for line in lines:
            if nm in line:
                start = line.index("SUBJECT(S): ") + len("SUBJECT(S): ")
                end = line.index(", IC")
                subjects_string = ", ".join(n_sjs)
                new_line = line[:start] + subjects_string + line[end:]
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)

        with open(databases["student_database.txt"], "w") as sd:
            sd.writelines(updated_lines)

    def accept_student_payment(nm):
        with open(databases["student_database.txt"], "r") as sd:
            lines = sd.readlines()

        for line in lines:
            if nm in line:
                level_start = line.index("LEVEL: Form ") + len("LEVEL: Form ")
                level_end = line.index(", SUBJECT(S):")
                level = int(line[level_start:level_end].strip())

                subjects_start = line.index("SUBJECT(S): ") + len("SUBJECT(S): ")
                subjects_end = line.index(", IC/PASSPORT:")
                subjects_of_student = line[subjects_start:subjects_end].strip()
                subjects_list = subjects_of_student.split(", ")

                lv_price = level * 1000
                subjects_price = sum(subjects.get(subject, 0) for subject in subjects_list)

                total_price = lv_price + subjects_price
                print(f"Student should pay: RM {total_price}")

                if input("Confirm payment (Yes/No): ").lower() == "yes":
                    receipt = f'''
----------Receipt----------
Excellent Tuition Centre (ETC)

Level price (Form {level})___RM {lv_price}
Subjects price:
'''
                    for subject in subjects_list:
                        receipt += f"{subject}___RM {subjects.get(subject, 0)}\n"

                    receipt += f'''
Overall total price = RM {total_price}
Payment status updated to paid
'''
                    print(receipt)

                    with open(databases["payment_status.txt"], "r") as pd:
                        lines = pd.readlines()

                    with open(databases["payment_status.txt"], "w") as pd:
                        pd.writelines(line for line in lines if nm.title() not in line)
                        pd.write(f"STUDENT NAME: {nm.title()}, PAYMENT STATUS: Paid\n")
                return

    def delete_student(nm):
        def update_file(file_path, name_format):
            with open(file_path, "r") as file:
                lines = file.readlines()
            with open(file_path, "w") as file:
                file.writelines(line for line in lines if name_format not in line)

        update_file(databases["main_database.txt"], nm.lower())
        update_file(databases["student_database.txt"], nm.title())
        update_file(databases["payment_status.txt"], nm.title())

    def change_profile(un, pw):
        try:
            with open(databases["main_database.txt"], "r+") as md:
                lines = md.readlines()
                md.seek(0)
                md.truncate()
                md.writelines(line for line in lines if un.lower().strip() not in line.lower().strip())
                md.write(f"USERNAME: {un.lower().strip()}, PASSWORD: {pw}, STATUS: Receptionist\n")

            print("Profile updated successfully.")
        except Exception as e:
            print(f"An error occurred while changing the profile: {e}")

    digits = string.digits

    def register_student():
        student_name = input("Enter student name: ")
        temporal_student_password = ''.join(random.choice(digits) for i in range(6))    

        print(subjects_list)
        chosen_subjects = [input(f"Enter subject {i + 1}: ").title() for i in range(3)]
        student_infos = [input(info) for info in ["IC/Passport: ", "Email: ", "Contact number: ", "Address: ", "Level: ", "Month of enrollment: "]]

        register_student_func(student_name, temporal_student_password, chosen_subjects, student_infos)

    def update_subject_enrollment_func():
        student_name = input("Student name: ")

        print(subjects_list)
        new_subjects = [input(f"New subject {i + 1}: ").title() for i in range(3)]
        update_subject_enrollment(student_name.title(), new_subjects)

    def accept_student_payment_func():
        student_name = input("Student name: ")
        accept_student_payment(student_name.title())

    def delete_student_func():
        delete_student(input("Student name: "))

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

    switch = {
        1: register_student,
        2: update_subject_enrollment_func,
        3: accept_student_payment_func,
        4: delete_student_func,
        5: update_profile,
        6: quit_program
    }

    print(receptionist_message)
    receptionist_function = int(input("Type (in number) which function to execute: "))

    func = switch.get(receptionist_function, lambda: print("Invalid input"))
    func()

if __name__ == "__main__":
    main()