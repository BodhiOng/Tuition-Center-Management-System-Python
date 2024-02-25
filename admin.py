# Import tutor/student subjects from another Python script
from income_report import subjects

# Define a function to register a new tutor
def register_tutor(nm, lv, sj, ps):
    # Check if tutor level is between 1-5 and tutor subject in option or not
    if lv not in range(1,6) or sj.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]:
        return
    
    # Check whether tutor had already existed in main_database.txt or not
    with open("main_database.txt", "r") as md:
        lines = md.readlines()
        for line in lines:
            if nm.lower() in line:
                return
    
    # Add the new tutor to main_database.txt
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Tutor")

    # Add the new tutor to tutor_database.txt
    with open("tutor_database.txt", "a") as td:
        td.write(f"\nTUTOR NAME: {nm.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'")

# Define a function to delete a tutor            
def delete_tutor(nm):
    # Read main_database.txt
    with open("main_database.txt", "r") as md:
        lines = md.readlines()

    # Write the updated main_database.txt without the tutor that was deleted
    with open("main_database.txt", "w") as md:
        for line in lines:
            if nm.lower() in line:
                continue    
            md.write(line)

    # Read tutor_database.txt
    with open("tutor_database.txt", "r") as td:
        lines = td.readlines()

    # Write the updated tutor_database.txt without the tutor that was deleted
    with open("tutor_database.txt", "w") as td:
        for line in lines:
            if nm.title() in line:
                continue    
            td.write(line)

# Define a function to register a new receptionist 
def register_receptionist(nm, ps):
    # Add the new receptionist to main_database.txt
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {nm.lower()}, PASSWORD: {ps}, STATUS: Receptionist")
    
    # Add the new receptionist to receptionist_database.txt
    with open("receptionist_database.txt", "a") as rd:
        rd.write(f"\nRECEPTIONIST NAME: {nm.title()}")

# Define a function to delete a receptionist
def delete_receptionist(nm):
    # Read main_database.txt
    with open("main_database.txt", "r") as md:
        lines = md.readlines()

    # Write the updated main_database.txt without the receptionist that was deleted
    with open("main_database.txt", "w") as md:
        for line in lines:
            if nm.lower() in line:
                continue    
            md.write(line)

    # Read receptionist_database.txt
    with open("receptionist_database.txt", "r") as rd:
        lines = rd.readlines()

    # Write the updated receptionist_database.txt without the receptionist that was deleted
    with open("receptionist_database.txt", "w") as rd:
        for line in lines:
            if nm.title() in line:
                continue    
            rd.write(line)

# Define a function to view the monthly income of a tutor
def view_monthly_income(nm, lv, sj):
    # Get the tutor's subject income & level income
    subject_income = subjects[sj.title()]
    level_income = lv * 1000

    # Calculate the tutor's total monthly income
    total_income= subject_income + level_income

    # Print the tutor's monthly income
    print(f"{nm.title()} monthly income: RM{total_income:.2f}")

# Define a function for admin to change their profile
def change_profile(un, pw):
    # Read main_database.txt
    with open("main_database.txt", "r") as md:
        lines = md.readlines()

    # Write the updated main_database.txt in which admin is (temporarily) removed
    with open("main_database.txt", "w") as md:
        for line in lines:
            if un.lower() in line:
                continue    
            md.write(line)

    # Write the more updated main_database.txt in which admin is added back again with their new password
    with open("main_database.txt", "a") as md:
        md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Admin")

# Admin message to show the functions they could use
admin_message = '''
\nAdmin functions:
1. Register/delete tutors
2. Register/delete the receptionist
3. View monthly income report of tutors
4. Update profile
'''
print(admin_message)

# Get the admin's choice of function to execute
admin_function = int(input("Type (in number) which function to execute: "))

if admin_function == 1:
    # Register/delete tutors
    # Ask whether admin wants to register or delete a tutor
    register_or_delete = input("Register (type R) or Delete (type D): ")

    if register_or_delete.lower() == "r":
        # Register a new tutor
        # Prompt for tutor's name, level, subject, and temporal password
        tutor_name = input("Tutor name: ")
        tutor_level = int(input("Tutor level (1-5): "))
        print("List of subjects: Bahasa Melayu, English Language, History, Mathematics, Science")
        tutor_subject = input("Tutor subject: ")
        temporal_tutor_password = input("Tutor temporal password (6-digits of number): ")

        register_tutor(tutor_name, tutor_level, tutor_subject, temporal_tutor_password)
    elif register_or_delete.lower() == "d":
        # Delete a tutor
        # Prompt for tutor's name
        tutor_name = input("Tutor name to delete: ")
        
        delete_tutor(tutor_name)
    else:
        # Admin inputted something else out of the option
        print("Invalid input")
elif admin_function == 2:
    # Register/delete the receptionist
    # Ask whether admin wants to register or delete a receptionist
    register_or_delete = input("Register (type R) or Delete (type D): ")

    if register_or_delete.lower() == "r":
        # Register a new receptionist
        # Prompt for receptionist name and temporal password
        receptionist_name = input("Receptionist name: ")
        temporal_receptionist_password = input("Receptionist temporal password (6-digits of number): ")

        register_receptionist(receptionist_name, temporal_receptionist_password)
    elif register_or_delete.lower() == "d":
        # Delete a receptionist
        # Prompt for receptionist password
        receptionist_name = input("Receptionist name: ")

        delete_receptionist(receptionist_name)
    else:
        # Admin inputted something else out of the option
        print("Invalid input")
elif admin_function == 3:
    # View the monthly income of a tutor (Suggestion: input prompts while reading tutor_database.txt)
    # Prompt for tutor's name, level, subject
    tutor_name = input("Tutor name: ")
    tutor_level = int(input("Tutor level (1-5): "))
    tutor_subject = input("Tutor subject: ")

    view_monthly_income(tutor_name, tutor_level, tutor_subject)
elif admin_function == 4:
    # Prompt for admin's username and new password (Suggestion: input prompts while reading main_database.txt)
    admin_username = input("Admin username: ")
    admin_new_password = input("Admin new password: ")

    change_profile(admin_username, admin_new_password)
else:
    # Admin inputted something else that is out of the option
    print("Invalid input")