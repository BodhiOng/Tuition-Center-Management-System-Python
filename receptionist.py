# Import tutor/student subjects from another Python script
from income_report import subjects

# Define a function to register a new student
def register_student(nm, ps, sjs, sd_i):
    # Check whether the typed subjects are a part of the options or not 
    for subject in sjs:
        if subject.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]:
            return

    # Check if typed month of enrollment and student's IC/passport number is valid or not
    if sd_i[5].title() not in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] or int(sd_i[4]) not in range(1,6):
        return

    # Add the student to main_database.txt   
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Student")

    # Add the student to student_database.txt
    with open("student_database.txt", "a") as sd:
        sd.write(f"\nSTUDENT NAME: {nm.title()}, LEVEL: Form {sd_i[4]}, SUBJECT(S): {sjs}, IC/PASSPORT: {sd_i[0]}, EMAIL: {sd_i[1]}, CONTACT NUMBER: {sd_i[2]}, ADDRESS: {sd_i[3]}, MONTH OF ENROLLMENT: {sd_i[5].title()} ")

    # Add the student to payment_status.txt
    with open("payment_status.txt", "a") as ps:
        ps.write(f"\nSTUDENT NAME: {nm.title()}, PAYMENT STATUS: Unpaid")


# Define a function to update a student's subject enrollment
def update_subject_enrollment(nm, n_sjs):
    # Read student_database.txt
    with open("student_database.txt", "r") as sd:
        lines = sd.readlines()

    # Find that student's old data and put it into the list
    old_data_list = []
    for line in lines:
        if nm in line:
            old_data_list.append(line)

    # Get the student's old subject enrollment data
    old_data_string = str(old_data_list[0])
    subjects_section_start, subjects_section_end = old_data_string.index("["), old_data_string.index(", IC")
    
    # Create a new data string with the student's new subject enrollment in it
    new_data_string = old_data_string[:subjects_section_start] + n_sjs + old_data_string[subjects_section_end:]

    # Write the updated student_database.txt in which the student with their old data is deleted
    with open("student_database.txt", "w") as sd:
        for line in lines:
            if nm in line:
                continue
            sd.write(line)

    # Write the more updated student_database.txt in which student is added back with their new data
    with open("student_database.txt", "a") as sd:
        sd.write(new_data_string)

# Define a function to accept student payment
def accept_student_payment(nm, lv, sj1, sj2, sj3):
    # Read student_database.txt
    with open("student_database.txt", "r") as sd:
        lines = sd.readlines()
    
    for line in lines:
        # Try to confirm that student's name is in student_database.txt
        if nm in line:
            # Determine price based on level and price based on the 3 chosen subjects
            lv_price = lv * 1000
            sj1_price, sj2_price, sj3_price = subjects[sj1], subjects[sj2], subjects[sj3]

            # Calculate all of the prices together and print statement of due payment
            total_price = lv_price + sj1_price + sj2_price + sj3_price
            print(f"Student should pay: RM {total_price}")

            # Prompt for confirmation of payment
            confirm_payment = input("Confirm payment (Yes/No): ")
            if confirm_payment.lower() == "yes":
                # Payment confirmed and receipt will be printed
                receipt_message = f'''
----------Receipt----------
Excellent Tuition Centre (ETC)

Level price (Form {str(lv)})___RM {lv_price}

Subjects price:
1. {sj1}___RM {sj1_price}
2. {sj2}___RM {sj2_price}
3. {sj3}___RM {sj3_price}

Overall total price = RM {total_price}
'''
                print(receipt_message)

                # Read payment_status.txt
                with open("payment_status.txt", "r") as pd:
                    lines = pd.readlines()
                
                # Temporarily remove student from payment_status.txt
                with open("payment_status.txt", "w") as pd:
                    for line in lines:
                        if nm.title() in line:
                            continue
                        pd.write(line)

                # Update payment_status.txt changing payment status to "paid"
                with open("payment_status.txt", "a") as pd:
                    pd.write(f"\nSTUDENT NAME: {nm.title()}, PAYMENT STATUS: Paid")
            else:
                # Payment is cancelled and nothing is printed
                return
        else:
            # Student's name not in student_database.txt
            return

# Define a function to delete student
def delete_student(nm):
    # Read main_database.txt
    with open("main_database.txt", "r") as md:
        lines = md.readlines()

    # Write the updated main_database.txt without the student that was deleted
    with open("main_database.txt", "w") as md:
        for line in lines:
            if nm.lower() in line:
                continue
            md.write(line)

    # Read student_database.txt
    with open("student_database.txt", "r") as sd:
        lines = sd.readlines()

    # Write the updated student_database.txt without the student that was deleted
    with open("student_database.txt", "w") as sd:
        for line in lines:
            if nm.title() in line:
                continue
            sd.write(line)

# Define a function to let receptionist change their profile
def change_profile(un, pw):
    # Read main_database.txt
    with open("main_database.txt", "r") as md:
        lines = md.readlines()

    # Write the updated main_database.txt in which receptionist is (temporarily) removed
    with open("main_database.txt", "w") as md:
        for line in lines:
            if un.lower() in line:
                continue
            md.write(line)

    # Write the more updated main_database.txt in which receptionist is added back again with their new password
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Receptionist")

# Receptionist message to show the functions they could use
receptionist_message = '''
\nReceptionist functions:
1. Register a student
2. Update subject enrollment
3. Accept payment from students
4. Delete students who had completed their studies
5. Update profile
'''
print(receptionist_message)

# Get the receptionist's choice of function to execute
receptionist_function = int(input("Type (in number) which function to execute: "))

# Execute the selected function
if receptionist_function == 1:
    # Register a student
    # Prompt for student's name and temporal password
    student_name = input("Enter student name: ")
    temporal_student_password = input("Student temporal password (6-digits of number): ")

    # Add subjects chosen by students to a list, right after prompting 3 of those subjects
    chosen_subjects = []
    inputted_subject_counter = 0
    print("List of subjects: Bahasa Melayu, English Language, History, Mathematics, Science")
    while inputted_subject_counter < 3:
        subject_choice = input(f"Enter subject {inputted_subject_counter + 1}: ")
        chosen_subjects.append(subject_choice.title())
        inputted_subject_counter += 1

    # Prompt for student's IC/Passport, email, contact number, address, level, and month of enrollment. Then add all of those informations to a list.
    student_infos = []
    ic_passport = input("IC/Passport: ")
    email = input("Email: ")
    contact_number = input("Contact number: ")
    address = input("Address: ")
    level = input("Level: ")
    month_of_enrollment = input("Month of enrollment: ")
    student_infos.extend([ic_passport, email, contact_number, address, level, month_of_enrollment])

    register_student(student_name, temporal_student_password, chosen_subjects, student_infos)
elif receptionist_function == 2:
    # Update subject enrollment (Suggestion: input prompts while reading student_database.txt)
    # Prompt for student's name and new subjects
    student_name = input("Student name: ")

    print("List of subjects: Bahasa Melayu, English Language, History, Mathematics, Science")
    new_subject_counter = 0
    new_subjects_list = []
    while new_subject_counter < 3:
        new_subject = input(f"New subject {new_subject_counter + 1}: ")
        new_subject_counter += 1
        new_subjects_list.append(new_subject.title())

    new_subjects_string = str(new_subjects_list)

    update_subject_enrollment(student_name.title(), new_subjects_string)
elif receptionist_function == 3:
    # Accept payment from students (Suggestion: input prompts while reading student_database.txt)
    # Prompt for student's name, level, subject 1-3 
    student_name = input("Student name: ")
    student_level = int(input("Student level: "))
    print("List of subjects: Bahasa Melayu, English Language, History, Mathematics, Science")
    subject_1 = input("Subject 1: ")
    subject_2 = input("Subject 2: ")
    subject_3 = input("Subject 3: ")
    
    accept_student_payment(student_name.title(), student_level, subject_1.title(), subject_2.title(), subject_3.title())
elif receptionist_function == 4:
    # Delete student
    # Prompt for student name
    student_name = input("Student name: ")

    delete_student(student_name)
elif receptionist_function == 5:
    # Change the profile of the receptionist (Suggestion: input prompts while reading main_database.txt)
    # Prompt for receptionist username and password
    receptionist_username = input("Receptionist username: ")
    receptionist_new_password = input("Receptionist new password: ")

    change_profile(receptionist_username, receptionist_new_password)
else:
    # Receptionist inputted something else out of the option
    print("Invalid input")