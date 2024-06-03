from peripheral_py_files.database_absolute_paths import databases
from peripheral_py_files.income_report import subjects

sjs = ["English Language Arts", "Tamil Language", "Malay Language"]
for sub in sjs:
    if not isinstance(sub, dict) or "subject" not in sub or sub["subject"].title() not in subjects:
        print(f"Invalid subject: {sub}. Subject not found in the subjects list.")
        