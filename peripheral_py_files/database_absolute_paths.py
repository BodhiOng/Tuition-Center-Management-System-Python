import os

txt_databases_dir = os.path.join(os.path.dirname(__file__), "..", "txt_databases")

databases = {
    "main_database.txt": os.path.join(txt_databases_dir, "main_database.txt"),
    "classes_database.txt": os.path.join(txt_databases_dir, "classes_database.txt"),
    "logged_in_users.txt": os.path.join(txt_databases_dir, "logged_in_users.txt"),
    "payment_status.txt": os.path.join(txt_databases_dir, "payment_status.txt"),
    "pending_requests.txt": os.path.join(txt_databases_dir, "pending_requests.txt"),
    "receptionist_database.txt": os.path.join(txt_databases_dir, "receptionist_database.txt"),
    "student_database.txt": os.path.join(txt_databases_dir, "student_database.txt"),
    "tutor_database.txt": os.path.join(txt_databases_dir, "tutor_database.txt")
}