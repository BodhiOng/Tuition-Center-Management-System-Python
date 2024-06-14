import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from peripheral_py_files.income_report import subjects
from peripheral_py_files.user_messages import tutor_message
from peripheral_py_files.database_absolute_paths import databases
from peripheral_py_files.user_messages import *

def main():
    def is_valid_subject(subject):
        return subject.title() in subjects

    def is_valid_level(level):
        return 1 <= level <= 5

    def is_valid_day(day):
        return day.title() in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    def input_class_info():
        tutor_name = input("Tutor name: ")
        print(subjects_list)
        return (
            tutor_name,
            input("Subject name: "),
            int(input("Level: ")),
            input("Class schedule (ETC not open on weekends): "),
            input("Start of session (24-hour format): "),
            input("End of session (24-hour format): ")
        )


    def add_class_information(nm, sj, lv, sd, ss_s, ss_e):
        if not (is_valid_subject(sj) and is_valid_level(lv) and is_valid_day(sd)):
            print("Invalid subject, level, or schedule day.")
            return

        try:
            with open(databases["classes_database.txt"], "a") as cd:
                cd.write(f"\nTUTOR NAME: {nm.title()}, SUBJECT: '{sj.title()}', CHARGE: RM {subjects[sj.title()] / 4}/session, LEVEL: Form {lv}, CLASS SCHEDULE: Every {sd.title()}, TIME OF SESSION: {ss_s} until {ss_e} ")
        
            print("Class information successfully added")
        except Exception as e:
            print(f"An error occurred while adding class information: {e}")

    def update_class_information(nm, sj, lv, sd, ss_s, ss_e):
        if not (is_valid_subject(sj) and is_valid_level(lv) and is_valid_day(sd)):
            print("Invalid subject, level, or schedule day.")
            return

        try:
            with open(databases["classes_database.txt"], "r") as cd:
                lines = cd.readlines()

            with open(databases["classes_database.txt"], "w") as cd:
                for line in lines:
                    if nm.title() not in line:
                        cd.write(line)

            with open(databases["classes_database.txt"], "a") as cd:
                cd.write(f"\nTUTOR NAME: {nm.title()}, SUBJECT: '{sj.title()}', Charge: RM {subjects[sj.title()] / 4}/session, Level: Form {lv}, Class schedule: Every {sd.title()}, Time of session: {ss_s} until {ss_e} ")

            print("Class information successfully updated")
        except Exception as e:
            print(f"An error occurred while updating class information: {e}")

    def delete_class_information(nm):
        try:
            with open(databases["classes_database.txt"], "r") as cd:
                lines = cd.readlines()

            with open(databases["classes_database.txt"], "w") as cd:
                for line in lines:
                    if nm.title() not in line:
                        cd.write(line)
            print("Class information successfully deleted")
        
        except Exception as e:
            print(f"An error occurred while deleting class information: {e}")

    def view_list_of_students(lv, sj):
        if not (is_valid_level(lv) and is_valid_subject(sj)):
            print("Invalid level or subject.")
            return

        try:
            list_of_students = []

            with open(databases["student_database.txt"], "r") as sd:
                lines = sd.readlines()

            for line in lines:
                if (f"Form {lv}") in line and sj.title() in line:
                    start_of_name = line.index("STUDENT NAME:") + len("STUDENT NAME: ")
                    end_of_name = line.index(", LEVEL:")
                    student_name = line[start_of_name:end_of_name]
                    list_of_students.append(student_name)

            print("List of students enrolled:", list_of_students)
        except Exception as e:
            print(f"An error occurred while viewing the list of students: {e}")

    def update_profile(un, pw, lv, sj):
        try:
            with open(databases["main_database.txt"], "r") as md:
                lines = md.readlines()

            with open(databases["main_database.txt"], "w") as md:
                for line in lines:
                    if un.lower() not in line:
                        md.write(line)

            with open(databases["main_database.txt"], "a") as md:
                md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Tutor")

            with open(databases["tutor_database.txt"], "r") as td:
                lines = td.readlines()

            with open(databases["tutor_database.txt"], "w") as td:
                for line in lines:
                    if un.title() not in line:
                        td.write(line)

            with open(databases["tutor_database.txt"], "a") as td:
                td.write(f"\nTUTOR NAME: {un.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'")

            with open(databases["classes_database.txt"], "r") as cd:
                lines = cd.readlines()

            with open(databases["classes_database.txt"], "w") as cd:
                for line in lines:
                    if un.title() not in line:
                        cd.write(line)

            print("Please add/modify class information separately using the 1st/2nd function")
            print("Profile successfully updated")
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
        print(tutor_message)
        try:
            tutor_function = int(input("Type (in number) which function to execute: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        switch = {
            1: lambda: add_class_information(*input_class_info()),
            2: lambda: update_class_information(*input_class_info()) if input("Would you like to update (type U) or delete (type D): ").lower() == "u" else delete_class_information(input("Tutor name: ")),
            3: lambda: view_list_of_students(int(input("Tutor level: ")), input("Tutor subject: ")),
            4: lambda: update_profile(
                input("Tutor username: "),
                input("Tutor new password: "),
                print(subjects_list),
                int(input("Tutor new level: ")),
                input("Tutor new subject: ")
            ),
            5: quit_program
        }

        func = switch.get(tutor_function, lambda: print("Invalid input"))
        func()