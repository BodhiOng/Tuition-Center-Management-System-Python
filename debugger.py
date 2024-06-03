from peripheral_py_files.database_absolute_paths import databases


un = 'bodhi'
pw = 'password'

with open(databases["main_database.txt"], "r+") as md:
    lines = md.readlines()
    md.seek(0)    
    md.truncate()
    md.writelines(line for line in lines if un.lower() not in line.lower())
    md.write(f"USERNAME: {un.lower()}, PASSWORD: {pw}, STATUS: Admin\n")