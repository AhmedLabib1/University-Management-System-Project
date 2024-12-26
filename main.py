from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Tables.students import StudentManagement
from Tables.departments import DepartmentManagement
from Tables.courses import CourseManagement
from Tables.lecturers import LecturerManagement
from Tables.teaching_assistants import TeachingAssistantsManagement
from Tables.tuition_fees import FeesManagement
from Tables.enrolls import EnrollsManagement
from Tables.pre_requisites import PreRequisitesManagement
from Tables.sections import SectionsManagement
from Tables.classrooms import ClassroomManagement

class University_Management_System:

    def __init__(self, root):
        self.root = root
        self.root.title("University Management System")
        self.root.geometry("800x608")

        # ================================ Tabs ================================
        self.tab_control = ttk.Notebook(self.root)

        # Create Tabs
        self.student_tab = Frame(self.tab_control)
        self.department_tab = Frame(self.tab_control)
        self.course_tab = Frame(self.tab_control)
        self.lecturer_tab = Frame(self.tab_control)
        self.teaching_assistant_tab = Frame(self.tab_control)
        self.tuition_tab = Frame(self.tab_control)
        self.enroll_tab = Frame(self.tab_control)
        self.pre_requisite_tab = Frame(self.tab_control)
        self.section_tab = Frame(self.tab_control)
        self.classroom_tab = Frame(self.tab_control)

        # Add tabs to notebook
        self.tab_control.add(self.student_tab, text="Student")
        self.tab_control.add(self.department_tab, text="Department")
        self.tab_control.add(self.course_tab, text="Course")
        self.tab_control.add(self.lecturer_tab, text="Lecturers")
        self.tab_control.add(self.teaching_assistant_tab, text="Teaching Assistants")
        self.tab_control.add(self.tuition_tab, text="Fees")
        self.tab_control.add(self.enroll_tab, text="Enrolls")
        self.tab_control.add(self.pre_requisite_tab, text="Pre Requisites")
        self.tab_control.add(self.section_tab, text="Sections")
        self.tab_control.add(self.classroom_tab, text="Classrooms")

        self.tab_control.pack(expand=1, fill="both")


        # ================================ Student Management ===============================
        self.student_management = StudentManagement(self.student_tab)
        
        # ================================ Department Management ============================
        self.department_management = DepartmentManagement(self.department_tab)

        # ================================ Course Management ================================
        self.course_management = CourseManagement(self.course_tab)

        # ================================ Lecturer Management ==============================
        self.lecture_management = LecturerManagement(self.lecturer_tab)

        # ================================ Teaching Assistant Management ====================
        self.teaching_assistant_management = TeachingAssistantsManagement(self.teaching_assistant_tab)

        # ================================ TuitionFee Management ============================
        self.tuition_fee_management = FeesManagement(self.tuition_tab)

        # ================================ Enroll Management ================================
        self.enroll_management = EnrollsManagement(self.enroll_tab)

        # ================================ Pre Requisite Management =========================
        self.pre_requisite_management = PreRequisitesManagement(self.pre_requisite_tab)

        # ================================ Section Management ===============================
        self.section_management = SectionsManagement(self.section_tab)

        # ================================ Classroom Management =============================
        self.classroom_management = ClassroomManagement(self.classroom_tab)

if __name__ == "__main__":
    root = Tk()
    app = University_Management_System(root)
    root.mainloop()
