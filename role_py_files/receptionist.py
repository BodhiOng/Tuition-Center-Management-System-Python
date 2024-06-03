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

        with open(databases["main_database.txt"], "a") as md:
            with open(databases["main_database.txt"], "r") as md_check:
                lines = md_check.readlines()
                for line in lines:
                    if nm.lower() in line.lower():
                        print("Student already exists.")
                        return
                
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
                start, end = line.index("["), line.index(", IC")
                new_line = line[:start] + n_sjs + line[end:]
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)

        with open(databases["student_database.txt"], "w") as sd:
            sd.writelines(updated_lines)

    def accept_student_payment(nm, lv, sj1, sj2, sj3):
        with open(databases["student_database.txt"], "r") as sd:
            lines = sd.readlines()

        for line in lines:
            if nm in line:
                lv_price = lv * 1000
                total_price = lv_price + sum(subjects[sj] for sj in [sj1, sj2, sj3])
                print(f"Student should pay: RM {total_price}")

                if input("Confirm payment (Yes/No): ").lower() == "yes":
                    receipt = f'''
    ----------Receipt----------
    Excellent Tuition Centre (ETC)

    Level price (Form {lv})___RM {lv_price}
    Subjects price:
    1. {sj1}___RM {subjects[sj1]}
    2. {sj2}___RM {subjects[sj2]}
    3. {sj3}___RM {subjects[sj3]}

    Overall total price = RM {total_price}
    '''
                    print(receipt)

                    with open(databases["payment_status.txt"], "r") as pd:
                        lines = pd.readlines()

                    with open(databases["payment_status.txt"], "w") as pd:
                        pd.writelines(line for line in lines if nm.title() not in line)
                        pd.write(f"\nSTUDENT NAME: {nm.title()}, PAYMENT STATUS: Paid")
                return

    def delete_student(nm):
        def update_file(file_path, name_format):
            with open(file_path, "r") as file:
                lines = file.readlines()
            with open(file_path, "w") as file:
                file.writelines(line for line in lines if name_format not in line)

        update_file(databases["main_database.txt"], nm.lower())
        update_file(databases["student_database.txt"], nm.title())

    def change_profile(un, pw):
        with open(databases["main_database.txt"], "r") as md:
            lines = md.readlines()
        with open(databases["main_database.txt"], "w") as md:
            md.writelines(line for line in lines if un.lower() not in line)
            md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Receptionist")

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
        new_subjects_string = str([input(f"New subject {i + 1}: ").title() for i in range(3)])
        update_subject_enrollment(student_name.title(), new_subjects_string)

    def accept_student_payment_func():
        student_name = input("Student name: ")
        student_level = int(input("Student level: "))
        subjects_input = [input(f"Subject {i + 1}: ").title() for i in range(3)]
        accept_student_payment(student_name.title(), student_level, *subjects_input)

    def delete_student_func():
        delete_student(input("Student name: "))

    def update_profile():
        change_profile(input("Receptionist username: "), input("Receptionist new password: "))

    switch = {
        1: register_student,
        2: update_subject_enrollment_func,
        3: accept_student_payment_func,
        4: delete_student_func,
        5: update_profile
    }

    print(receptionist_message)
    receptionist_function = int(input("Type (in number) which function to execute: "))

    func = switch.get(receptionist_function, lambda: print("Invalid input"))
    func()

if __name__ == "__main__":
    main()