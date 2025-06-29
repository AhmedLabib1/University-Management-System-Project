# University Management System

This project is a **Graphical User Interface (GUI)** application built using **Python's Tkinter library**. It is designed to manage various components of a university system, such as courses, departments, students, tuition fees, enrollments, prerequisites, lecturers, teaching assistants, sections, and classrooms.

---

## **Features**
- **Tabbed Interface**: Organizes the system into easy-to-navigate tabs.
- **Modular Design**: Each management system (e.g., Courses, Departments, Students) is implemented as a separate class for scalability and maintainability.
- **Clean GUI**: User-friendly interface using Tkinter.

---

## **Project Structure**
```
University_Management_System GUI/
│
├── main.py                      # Main application file
├── README.md                    # Project documentation
│
├── Database/                    # Folder containing database configurations
│   ├── connection.py            # Database connection setup
│   └── setup.sql                # SQL script for database setup
│
├── Tables/                      # Folder containing management classes
│   ├── courses.py               # Course Management
│   ├── departments.py           # Department Management
│   ├── students.py              # Student Management
│   ├── tuition_fees.py          # Tuition Fees Management
│   ├── enrolls.py               # Enrolls Management
│   ├── pre_requisites.py        # Prerequisites Management
│   ├── lecturers.py             # Lecturer Management
│   ├── teaching_assistants.py   # Teaching Assistant Management
│   ├── sections.py              # Section Management
│   └── classrooms.py            # Classroom Management
│
└── __pycache__/                 # Python cache files
```
