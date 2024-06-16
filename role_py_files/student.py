import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from peripheral_py_files.income_report import subjects
from peripheral_py_files.user_messages import student_message, subjects_list
from peripheral_py_files.database_absolute_paths import databases

def main():
    def get_logged_in_student_details():
        try:
            username = ""
            with open(databases["logged_in_users.txt"], "r") as liu: 
                for line in liu:
                    if "(" in line:
                        username = line.split()[0]
                        break

            if not username:
                print("No logged-in user found")
                return None, None, None

            with open(databases["student_database.txt"], "r") as sd:
                for line in sd:
                    if username.title() in line:
                        level_start = line.index("LEVEL: Form ") + len("LEVEL: Form ")
                        level_end = line.index(", SUBJECT(S):")
                        level = int(line[level_start:level_end].strip())

                        subjects_start = line.index("SUBJECT(S): ") + len("SUBJECT(S): ")
                        subjects_end = line.index(", IC/PASSPORT:")
                        subjects_of_student = line[subjects_start:subjects_end].strip()
                        subjects_list = subjects_of_student.split(", ")
                        return username, level, subjects_list

            print("Student details not found in the database")
            return None, None, None

        except Exception as e:
            print(f"An error occurred while retrieving student details: {e}")
            return None, None, None

    def view_schedule():
        try:
            username, level, subjects_list = get_logged_in_student_details()
            if username is None:
                return

            found_classes = False
            with open(databases["classes_database.txt"], "r") as cd:
                for line in cd:
                    if f"Form {level}" in line and any(subject in line for subject in subjects_list):
                        print(line.strip())
                        found_classes = True

            if not found_classes:
                print("No classes found")
        except Exception as e:
            print(f"An error occurred while viewing schedule: {e}")

    def send_request(new_subjects_list):
        try:
            username, _, _= get_logged_in_student_details()
            if username is None or new_subjects_list is None:
                return

            for subject in new_subjects_list:
                if subject.title() not in subjects.keys():
                    print("Subject input is invalid")
                    return
                
            with open(databases["student_database.txt"], "r") as sd:
                student_found = any(username.title() in line for line in sd)
                if not student_found:
                    print("Student Name not in Database")
                    return

            with open(databases["pending_requests.txt"], "a") as pr:
                subject_str = ", ".join(new_subjects_list)
                pr.write(f"{username.title()} requested change of enrolled subject into {subject_str}\n")
            print("Request is sent, please wait for receptionist's update.")
        except Exception as e:
            print(f"An error occurred while sending request: {e}")

    def delete_request(name):
        try:
            with open(databases["pending_requests.txt"], "r") as pr:
                lines = pr.readlines()
            with open(databases["pending_requests.txt"], "w") as pr:
                for line in lines:
                    if name.title() not in line:
                        pr.write(line)
            print("Request successfully deleted")
        except Exception as e:
            print(f"An error occurred while deleting request: {e}")

    def view_payment_status(name, subjects_list):
        try:
            with open(databases["payment_status.txt"], "r") as ps:
                for line in ps:
                    if name.title() in line:
                        payment_status = line.split("PAYMENT STATUS: ")[-1].strip()
                        if payment_status == "Unpaid":
                            total_balance = sum(subjects.get(subj.title(), 0) for subj in subjects_list)
                            print(f"PAYMENT STATUS: Unpaid, TOTAL BALANCE DUE: RM {total_balance}")
                        else:
                            print("PAYMENT STATUS: Paid")
                        return
                print("Name not in database")
        except Exception as e:
            print(f"An error occurred while viewing payment status: {e}")

    def change_profile(username, password, student_info):
        try:
            with open(databases["main_database.txt"], "r") as md:
                lines = md.readlines()
            with open(databases["main_database.txt"], "w") as md:
                md.writelines(line for line in lines if username.lower() not in line)
                md.write(f"USERNAME: {username.lower()}, PASSWORD: {password}, STATUS: Receptionist\n")
            with open(databases["student_database.txt"], "r") as sd:
                lines = sd.readlines()
            subjects_list = []
            with open(databases["student_database.txt"], "w") as sd:
                for line in lines:
                    if username.title() in line:
                        subject_start = line.index("SUBJECT(S): [") + len("SUBJECT(S): [")
                        subject_end = line.index("], IC/PASSPORT:")
                        subjects_list.append(line[subject_start:subject_end])
                        continue
                    sd.write(line)
                sd.write(f"STUDENT NAME: {username.title()}, LEVEL: Form {student_info[4]}, SUBJECT(S): {subjects_list[0]}, IC/PASSPORT: {student_info[0]}, EMAIL: {student_info[1]}, CONTACT NUMBER: {student_info[2]}, ADDRESS: {student_info[3]}, MONTH OF ENROLLMENT: {student_info[5].title()} ")
            print("Profile successfully updated")
        except Exception as e:
            print(f"An error occurred while changing profile: {e}")

    def handle_send_request():
        print(subjects_list)
        new_sj_list = [input(f"Subject {i}: ").title() for i in range(1, 4)]
        send_request(new_sj_list)

    while True:
        print(student_message)

        try:
            student_function = int(input("Type (in number) which function to execute: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        switch = {
            1: lambda: view_schedule(),
            2: lambda: handle_send_request(),
            3: lambda: delete_request(input("Student name: ")),
            4: lambda: view_payment_status(input("Student name: "), [input(f"Subject {i}: ").title() for i in range(1, 4)]),
            5: lambda: change_profile(
                input("Student username: "),
                input("Student new password: "),
                [input("IC/Passport: "), input("Email: "), input("Contact number: "), input("Address: "), input("Level: "), input("Month of enrollment: ")]
            )
        }

        func = switch.get(student_function, lambda: print("Invalid input"))
        func()

if __name__ == "__main__":
    main()