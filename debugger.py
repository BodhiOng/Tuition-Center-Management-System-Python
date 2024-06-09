from peripheral_py_files.database_absolute_paths import databases
from peripheral_py_files.income_report import subjects

with open(databases["student_database.txt"], "r") as sd:
    lines = sd.readlines()
    for line in lines:
        if "Kandis" in line:
            level_start = line.index("LEVEL: Form ") + len("LEVEL: Form ")
            level_end = line.index(", SUBJECT(S):")
            level = line[level_start:level_end]

            subjects_start = line.index("SUBJECT(S): ") + len("SUBJECT(S): ")
            subjects_end = line.index(", IC/PASSPORT:")
            subjects = line[subjects_start:subjects_end]
            subjects_list = subjects.split(", ")
            sj1, sj2, sj3 = subjects_list

            print(sj1)
            print(sj2)
            print(sj3)