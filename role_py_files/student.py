# Import tutor/student subjects from another Python script
from peripheral_py_files.income_report import subjects

def main():
    # Define a function for student to view their classes
    def view_schedule(lv, sjs):
        # Read classes_database.txt
        with open("classes_database.txt", "r") as cd:
            lines = cd.readlines()

        # Checks every line containing specified level and subjects, also prints the schedule for viewing
        print("---Schedule---")
        for line in lines:
            for subject in sjs:
                if ("Form " + str(lv)) in line and subject in line:
                    print(line.strip()) 

    # Define a function for student to send request to change subject enrollment
    def send_request(nm, sjs):
        with open("student_database.txt", "r") as sd:
            lines = sd.readlines()

        # Confirms whether requester is a student or not
        for line in lines:
            if nm.title() not in line:
                print("Student Name not in Database")
                return

        # Confirms whether inputted subjects are valid or not
        for subject in sjs:
            if subject.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]:
                print("Subject input is invalid")
                return
        
        # Append request into pending_requests.txt 
        with open("pending_requests.txt", "a") as pr:
            pr.write(f"{nm.title()} requested change of enrolled subject into {sjs}\n")

        # Tell user that his/her request is already included in pending_requests.txt
        print("Request is sent, please wait for receptionist's update.")

    # Define a function for student to delete the pending request of change
    def delete_request(nm):
        with open("pending_requests.txt", "r") as pr:
            lines = pr.readlines()

        with open("pending_requests.txt", "w") as pr:
            for line in lines:
                if nm.title() in line:
                    continue
                pr.write(line)

    # Define a function for student to view payment status with due balance
    def view_payment_status(nm, sjs):
        # Read payment_status.txt
        with open("payment_status.txt", "r") as ps:
            lines = ps.readlines()

        # Check the payment status of the student
        for line in lines:
            if nm.title() in line:
                payment_status_section_start, payment_status_section_end = line.index("PAYMENT STATUS: ") + len("PAYMENT STATUS: "), len(line)
                if line[payment_status_section_start:payment_status_section_end] == "Unpaid":
                    # Payment status is unpaid
                    try:
                        total_balance = float(subjects[sjs[0]] + subjects[sjs[1]] + subjects[sjs[2]])
                    except:
                        print("Invalid Subject(s)")
                        exit()
                    print(f"PAYMENT STATUS: Unpaid, TOTAL BALANCE DUE: RM {total_balance}")
                else:
                    # Payment status is paid
                    print("PAYMENT STATUS: Paid")
            else:
                print("Name not in database")

    # Define a function for student to change their profile
    def change_profile(un, pw, sd_i):
        # Read main_database.txt
        with open("main_database.txt", "r") as md:
            lines = md.readlines()

        # Write the updated main_database.txt in which student is (temporarily) removed
        with open("main_database.txt", "w") as md:
            for line in lines:
                if un.lower() in line:
                    continue
                md.write(line)

        # Write the more updated main_database.txt in which student is added back again with their new password
        with open("main_database.txt", "a") as md:
            md.write(f"USERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Receptionist")

        # Read student_database.txt
        with open("student_database.txt", "r") as sd:
            lines = sd.readlines()
        
        # Initializes empty list to store student's subjects
        subjects_list = []

        # Append student's subjects to previous list & temporarily remove student from student_database.txt
        with open("student_database.txt", "w") as sd:
            for line in lines:
                if un.title() in line:
                    subject_section_start, subject_section_end = line.index("SUBJECT(S): [") + len("SUBJECT(S): ["), line.index("], IC/PASSPORT:")
                    subjects_list.append(line[subject_section_start:subject_section_end])
                    continue
                sd.write(line)

        # Add the student back to student_database.txt with new data
        with open("student_database.txt", "a") as sd:
            sd.write(f"STUDENT NAME: {un.title()}, LEVEL: Form {sd_i[4]}, SUBJECT(S): {subjects_list[0]}, IC/PASSPORT: {sd_i[0]}, EMAIL: {sd_i[1]}, CONTACT NUMBER: {sd_i[2]}, ADDRESS: {sd_i[3]}, MONTH OF ENROLLMENT: {sd_i[5].title()} ")

    # Tutor message to show the functions they could use

    print(student_message)

    # Get the student's choice of function to execute
    student_function = int(input("Type (in number) which function to execute: "))

    if student_function == 1:
        # View schedule of classes (Suggestion: input prompts while reading student_database.txt)
        # Prompt for student's level
        student_level = int(input("Student level: "))

        # Prompt for all three student subjects
        student_subjects = []
        for i in range(1, 4):
            prompt_subject = input(f"Subject {i}: ")
            student_subjects.append(prompt_subject.title())

        view_schedule(student_level, student_subjects)
    elif student_function == 2:
        # Request receptionist for change on enrolled subject
        # Prompt for student name
        student_name = input("Student name: ")

        # Tell user that the 3 inputted subjects doesn't have to be all new subjects
        print("Input existing/the same subject if that subject want to be kept")

        # Prompt for all three new student subjects
        student_subjects = []
        for i in range(1,4):
            prompt_subject = input(f"Subject {i}: ")
            student_subjects.append(prompt_subject.title())

        send_request(student_name, student_subjects)
    elif student_function == 3:
        # Prompt for student name
        student_name = input("Student name: ")

        delete_request(student_name)
    elif student_function == 4:
        # View payment status (Suggestion: input prompts while reading student_database.txt)
        # Prompt for student name
        student_name = input("Student name: ")

        # Prompt for all three student subjects
        student_subjects = []
        for i in range(1,4):
            prompt_subject = input(f"Subject {i}: ")
            student_subjects.append(prompt_subject.title())

        view_payment_status(student_name, student_subjects)
    elif student_function == 5:
        # Let student update their profile (Suggestion: input prompts while reading student_database.txt)
        # Print message to tell student that they don't have to type new informations for all the prompts
        print("Type the same information if you don't want to modify them.")

        # Prompt for student username and password
        student_username = input("Student username: ")
        student_new_password = input("Student new password: ")

        # Prompt for student's IC/Passport, email, contact number, address, level, and month of enrollment. Then add all of those informations to a list.
        student_infos = []
        ic_passport = input("IC/Passport: ")
        email = input("Email: ")
        contact_number = input("Contact number: ")
        address = input("Address: ")
        level = input("Level: ")
        month_of_enrollment = input("Month of enrollment: ")
        student_infos.extend([ic_passport, email, contact_number, address, level, month_of_enrollment])

        change_profile(student_username, student_new_password, student_infos)
    else:
        # Student inputted something else put of the option
        print("Invalid input")
