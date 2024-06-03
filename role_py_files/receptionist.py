from peripheral_py_files.income_report import subjects
from peripheral_py_files.user_messages import receptionist_message

def main():
    def register_student(nm, ps, sjs, sd_i):
        valid_subjects = ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]
        valid_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        if not all(sub.title() in subjects for sub in sjs):
            print(f"Invalid subject: {sjs}. Subject not found in the subjects list.")
            return

        if sd_i[5].title() not in valid_months or not 1 <= int(sd_i[4]) <= 5:
            return

        with open("main_database.txt", "a") as md:
            md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Student")

        with open("student_database.txt", "a") as sd:
            sd.write(f"\nSTUDENT NAME: {nm.title()}, LEVEL: Form {sd_i[4]}, SUBJECT(S): {sjs}, IC/PASSPORT: {sd_i[0]}, EMAIL: {sd_i[1]}, CONTACT NUMBER: {sd_i[2]}, ADDRESS: {sd_i[3]}, MONTH OF ENROLLMENT: {sd_i[5].title()} ")

        with open("payment_status.txt", "a") as ps:
            ps.write(f"\nSTUDENT NAME: {nm.title()}, PAYMENT STATUS: Unpaid")

    def update_subject_enrollment(nm, n_sjs):
        with open("student_database.txt", "r") as sd:
            lines = sd.readlines()

        updated_lines = []
        for line in lines:
            if nm in line:
                start, end = line.index("["), line.index(", IC")
                new_line = line[:start] + n_sjs + line[end:]
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)

        with open("student_database.txt", "w") as sd:
            sd.writelines(updated_lines)

    def accept_student_payment(nm, lv, sj1, sj2, sj3):
        with open("student_database.txt", "r") as sd:
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

                    with open("payment_status.txt", "r") as pd:
                        lines = pd.readlines()

                    with open("payment_status.txt", "w") as pd:
                        pd.writelines(line for line in lines if nm.title() not in line)
                        pd.write(f"\nSTUDENT NAME: {nm.title()}, PAYMENT STATUS: Paid")
                return

    def delete_student(nm):
        def update_file(file_path, name_format):
            with open(file_path, "r") as file:
                lines = file.readlines()
            with open(file_path, "w") as file:
                file.writelines(line for line in lines if name_format not in line)

        update_file("main_database.txt", nm.lower())
        update_file("student_database.txt", nm.title())

    def change_profile(un, pw):
        with open("main_database.txt", "r") as md:
            lines = md.readlines()
        with open("main_database.txt", "w") as md:
            md.writelines(line for line in lines if un.lower() not in line)
            md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Receptionist")

    def register_student():
        student_name = input("Enter student name: ")
        temporal_student_password = input("Student temporal password (6-digits of number): ")

        chosen_subjects = [input(f"Enter subject {i + 1}: ").title() for i in range(3)]
        student_infos = [input(info) for info in ["IC/Passport: ", "Email: ", "Contact number: ", "Address: ", "Level: ", "Month of enrollment: "]]

        register_student(student_name, temporal_student_password, chosen_subjects, student_infos)

    def update_subject_enrollment():
        student_name = input("Student name: ")
        new_subjects_string = str([input(f"New subject {i + 1}: ").title() for i in range(3)])
        update_subject_enrollment(student_name.title(), new_subjects_string)

    def accept_student_payment():
        student_name = input("Student name: ")
        student_level = int(input("Student level: "))
        subjects_input = [input(f"Subject {i + 1}: ").title() for i in range(3)]
        accept_student_payment(student_name.title(), student_level, *subjects_input)

    def delete_student():
        delete_student(input("Student name: "))

    def update_profile():
        change_profile(input("Receptionist username: "), input("Receptionist new password: "))

    switch = {
        1: register_student,
        2: update_subject_enrollment,
        3: accept_student_payment,
        4: delete_student,
        5: update_profile
    }

    print(receptionist_message)
    receptionist_function = int(input("Type (in number) which function to execute: "))

    func = switch.get(receptionist_function, lambda: print("Invalid input"))
    func()

if __name__ == "__main__":
    main()