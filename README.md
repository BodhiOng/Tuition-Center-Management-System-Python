# Tuition Center Management System (CLI-based program)

This project is a Python-based Tuition Centre Management System developed as part of the CT108-3-1 Python Programming Group Assignment for the Asia Pacific University of Technology and Innovation in 2023. For further clarity on functionalities and what this program does please read [PYP Assignment Briefing From Lecturer](https://github.com/BodhiOng/Programming-With-Python-Semester-1-Assignment/blob/main/Assignment%20Briefing%20%26%20Report/PYP%20Assignment%20Briefing%20From%20Lecturer.pdf) and [PYP Report](https://github.com/BodhiOng/Programming-With-Python-Semester-1-Assignment/blob/main/Assignment%20Briefing%20%26%20Report/PYP%20Report.docx). 

## How to run the program
Run `login.py` and log in with the username & password in `main_database.txt`. Note that each one of the .py roles is connected to certain .txt files in which the direct relation could be seen by reading the functions in the script or assessing the comments typed. Thus, if further inputs are required from the role before executing the functionality, please fill the inputs with information that is available on the .txt files unless the prompt demands an input that is different from the original information, just follow the given instructions accordingly. 

## Project description
The Tuition Centre Management System aims to provide functionalities for different types of users within the system, including Admins, Receptionists, Tutors, and Students. Each user role has specific tasks and features they can perform within the system.

## User Roles and Functionalities
### Admin
- Register and delete tutors. Assign tutors to respective levels and subjects.
- Register and delete the receptionist.
- View monthly income report based on level and subject.
- Update own profile.
### Receptionist
- Register a student and enroll the student in up to 3 subjects. During enrolment, record
student information for eg: name, IC/Passport, email, contact number, address, level,
subjects, the month of enrolment, etc (you may add other relevant information)
- Update subject enrollment if students request to change subject.
- Accept payment from students and generate receipts.
- Delete students who have completed their studies.
- Update own profile.
### Tutor
- Add class information (e.g. subject name, charges, class schedule, etc) .
- Update and delete class information.
- View the list of students enrolled in his/her subjects.
- Update own profile.
### Student
- View the schedule of his/her classes.
- Send a request to the receptionist to change the enrolled subject.
- Delete the request (which is still pending) sent to the receptionist to change the subject.
- View payment status with the total balance that needs to be paid, if any.
- Update own profile.
