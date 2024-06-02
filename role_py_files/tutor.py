# Import tutor/student subjects from another Python script
from peripheral_py_files.income_report import subjects

# Define a function to add class information
def add_class_information(nm, sj, lv, sd, ss_s, ss_e):
   # Check whether inputted subject, level, class schedule are valid or not
   if sj.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"] or lv not in range(1,6) or sd.title() not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
      return

   # Write the updated classes_database.txt with the new class information
   with open("classes_database.txt", "a") as cd:
      cd.write(f"\nTUTOR NAME: {nm.title()}, SUBJECT: '{sj.title()}', CHARGE: RM {str(subjects[sj.title()]/4)}/session, LEVEL: Form {lv}, CLASS SCHEDULE: Every {sd.title()}, TIME OF SESSION: {ss_s} until {ss_e} ")

# Define a function to update class information
def update_class_information(nm, sj, lv, sd, ss_s, ss_e):

   # Check whether inputted subject, level, class schedule are valid or not
   if sj.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"] or lv not in range(1,6) or sd.title() not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
      return

   # Read classes_database.txt
   with open("classes_database.txt", "r") as cd:
      lines = cd.readlines()

   # Write the updated classes_database.txt in which class information is (temporarily) removed
   with open("classes_database.txt", "w") as cd:
      for line in lines:
         if nm.title() in line:
               continue    
         cd.write(line)

   # Write the updated classes_database.txt with the new class information
   with open("classes_database.txt", "a") as cd:
      cd.write(f"\nTUTOR NAME: {nm.title()}, SUBJECT: '{sj.title()}', Charge: RM {str(subjects[sj.title()]/4)}/session, Level: Form {lv}, Class schedule: Every {sd.title()}, Time of session: {ss_s} until {ss_e} ")

# Define a function to delete class information
def delete_class_information(nm):
   # Read classes_database.txt
   with open("classes_database.txt", "r") as cd:
      lines = cd.readlines()

   # Write the updated classes_database.txt in which class information is removed
   with open("classes_database.txt", "w") as cd:
      for line in lines:
         if nm.title() in line:
            continue
         cd.write(line)

# Define a function to view list of students enrolled in a certain subject and on a certain level   
def view_list_of_students(lv, sj):
   # Read student_database.txt"
   with open("student_database.txt", "r") as sd:
      lines = sd.readlines()

   # Confirms whether level and subject is valid
   if lv not in range(1,6) or sj.title() not in ["Bahasa Melayu", "English Language", "History", "Mathematics", "Science"]:
      return

   # Initializes an empty list as a repository for student names
   list_of_students = []

   # Append student names into the previous list
   for line in lines:
      if ("Form " + str(lv)) in line and sj.title() in line:
         start_of_name = line.index("STUDENT NAME:") + len("STUDENT NAME: ")
         end_of_name = line.index(", LEVEL:")
         student_name = line[start_of_name:end_of_name]
         list_of_students.append(student_name)

   # Print the list of students enrolled
   print("List of students enrolled:", str(list_of_students))

# Define a function to update the profile of the tutor
def update_profile(un, pw, lv, sj):   
   # Read main_database.txt
   with open("main_database.txt", "r") as md:
      lines = md.readlines()

   # Write the updated main_database.txt in which tutor is (temporarily) removed
   with open("main_database.txt", "w") as md:
      for line in lines:
         if un.lower() in line:
               continue
         md.write(line)

   # Write the more updated main_database.txt in which tutor is added back again with their new password
   with open("main_database.txt", "a") as md:
      md.write(f"\nUSERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Tutor")

   # Read tutor_database.txt
   with open("tutor_database.txt", "r") as td:
      lines = td.readlines()

   # Write the updated tutor_database.txt in which tutor is (temporarily) removed
   with open("tutor_database.txt", "w") as td:
      for line in lines:
         if un.title() in line:
               continue
         td.write(line)

   # Write the more updated tutor_database.txt in which tutor is added back again with their new level & subject
   with open("tutor_database.txt", "a") as td:
      td.write(f"\nTUTOR NAME: {un.title()}, LEVEL: Form {lv}, SUBJECT: '{sj.title()}'")

   # Read classes_database.txt
   with open("classes_database.txt", "r") as cd:
      lines = cd.readlines()

   # Write the updated classes_database.txt in which tutor with their class is removed
   with open("classes_database.txt", "w") as cd:
      for line in lines:
         if un.title() in line:
               continue
         cd.write(line)

   # Inform the tutor that class information should be modified separately
   print("Please add/modify class information separately using the 1st/2nd function")
   
# Tutor message to show the functions they could use

print(tutor_message)

# Get the tutor's choice of function to execute
tutor_function = int(input("Type (in number) which function to execute: "))

if tutor_function == 1:
   # Add class information
   # Prompt for tutor name, subject name, session charge, level, class schedule, start of session and end of session
   tutor_name = input("Tutor name: ")
   subject_name = input("Subject name: ")
   level_taught = int(input("Level: "))
   weekly_schedule = input("Class schedule (ETC not open on weekends): ")
   session_start = input("Start of session (24-hour format): ")
   session_end = input("End of session (24-hour format): ")

   add_class_information(tutor_name, subject_name, level_taught, weekly_schedule, session_start, session_end)
elif tutor_function == 2:
   # Update/delete class information
   # Prompt whether user wants to update or delete
   update_or_delete = input("Would you like to update (type U) or delete (type D): ")

   if update_or_delete.lower() == "u":
      # Update class information (Suggestion: input prompts while reading classes_database.txt)
      # Prompt for tutor name, subject name, session charge, level, class schedule, start of session and end of session
      tutor_name = input("Tutor name: ")
      subject_name = input("Subject name: ")
      level_taught = int(input("Level: "))
      weekly_schedule = input("Class schedule (ETC not open on weekends): ")
      session_start = input("Start of session (24-hour format): ")
      session_end = input("End of session (24-hour format): ")

      update_class_information(tutor_name, subject_name, level_taught, weekly_schedule, session_start, session_end)

   elif update_or_delete.lower() == "d":
      # Delete class information
      # Prompt for tutor name
      tutor_name = input("Tutor name: ")

      delete_class_information(tutor_name)

   # Tutor typed something out of the option
   else:
      print("Invalid input")
elif tutor_function == 3:
   # View list of students enrolled in your subject (Suggestion: input prompts while reading tutor_database.txt or classes_database.txt)
   # Prompt for tutor level & tutor subject
   tutor_level = int(input("Tutor level: ") )
   tutor_subject = input("Tutor subject: ")

   view_list_of_students(tutor_level, tutor_subject)
elif tutor_function == 4:
   # Change the profile of the tutor (Suggestion: input prompts while reading tutor_database.txt)
   # Print message to inform tutor that it's ok to not modify everything
   print("Type the same information if info wasn't meant to be modified")

   # Prompt for username and new password (for main_database.txt modifications)
   tutor_username = input("Tutor username: ")
   tutor_new_password = input("Tutor new password: ")

   # Prompt for new level & new subject (for tutor_database.txt modifications)
   tutor_new_level = int(input("Tutor new level: "))
   tutor_new_subject = input("Tutor new subject: ")

   update_profile(tutor_username, tutor_new_password, tutor_new_level, tutor_new_subject)
else:
   # Tutor inputted something else out of the option
   print("Invalid input")