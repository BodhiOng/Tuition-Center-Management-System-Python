from peripheral_py_files.database_absolute_paths import databases
from peripheral_py_files.income_report import subjects

username = "glenn"
with open(databases["logged_in_users.txt"], "r") as liu: 
    for line in liu:
        if "(" in line:
            username = line.split()[0]
            break

if username:
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

                print(level, subjects_list)
                break
else:
    print("No logged-in user found")