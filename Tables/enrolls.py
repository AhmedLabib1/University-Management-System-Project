from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class EnrollsManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.enroll_id = StringVar()
        self.student_id = StringVar()
        self.course_id = StringVar()
        self.pre_requisite = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Enrolls Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=130)

        Label(form_frame, text="Enroll ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)  # New field
        ttk.Entry(form_frame, textvariable=self.enroll_id, font=('Arial', 12), width=25).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Student ID", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.student_id, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="Course ID", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_id, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Pre-Requisite (T/F)", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.pre_requisite, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_enrollment, font=('Arial', 12), bg='green', fg='white').grid(row=2, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_enrollment, font=('Arial', 12), bg='blue', fg='white').grid(row=2, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_enrollment, font=('Arial', 12), bg='red', fg='white').grid(row=2, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=2, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=190, width=780, height=390)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.enrolls_table = ttk.Treeview(table_frame, columns=("Enroll ID", "Student ID", "Course ID", "Pre-Requisite"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.enrolls_table.xview)
        scroll_y.config(command=self.enrolls_table.yview)

        self.enrolls_table.heading("Enroll ID", text="Enroll ID")  # New column
        self.enrolls_table.heading("Student ID", text="Student ID")
        self.enrolls_table.heading("Course ID", text="Course ID")
        self.enrolls_table.heading("Pre-Requisite", text="Pre-Requisite")

        self.enrolls_table.column("Enroll ID", width=100, anchor=CENTER)  # New column width
        self.enrolls_table.column("Student ID", width=100, anchor=CENTER)
        self.enrolls_table.column("Course ID", width=150, anchor=CENTER)
        self.enrolls_table.column("Pre-Requisite", width=150, anchor=CENTER)

        self.enrolls_table['show'] = 'headings'
        self.enrolls_table.pack(fill=BOTH, expand=1)
        self.enrolls_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_enrollments()

    # ================================ Database Operations ================================
    def connect_db(self):
        try:
            # Connection string for SQL Server
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost;'  # Your SQL Server instance
                'DATABASE=University_DB5;'  # Your DB name
                'Trusted_Connection=yes;'  # Use Windows Authentication
            )
            return connection
        except pyodbc.Error as err:
            messagebox.showerror("Connection Error", f"Error: {err}")
            return None

    def fetch_enrollments(self):
        self.enrolls_table.delete(*self.enrolls_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enrolls")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.enrolls_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching enrollments: {str(e)}")

    def add_enrollment(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO enrolls (Enroll_ID, Student_ID, Course_ID, Pre_Requisite) VALUES (?, ?, ?, ?)",
                           (self.enroll_id.get(), self.student_id.get(), self.course_id.get(), self.pre_requisite.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Enrollment added successfully!")
            self.fetch_enrollments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding enrollment: {str(e)}")

    def update_enrollment(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE enrolls SET Student_ID=?, Course_ID=?, Pre_Requisite=? WHERE Enroll_ID=?",
                           (self.student_id.get(), self.course_id.get(), self.pre_requisite.get(), self.enroll_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Enrollment updated successfully!")
            self.fetch_enrollments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating enrollment: {str(e)}")

    def delete_enrollment(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enrolls WHERE Enroll_ID=?", 
                           (self.enroll_id.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Enrollment deleted successfully!")
            self.fetch_enrollments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting enrollment: {str(e)}")

    def clear_fields(self):
        self.enroll_id.set("")
        self.student_id.set("")
        self.course_id.set("")
        self.pre_requisite.set("")

    def get_cursor(self, event):
        cursor_row = self.enrolls_table.focus()
        content = self.enrolls_table.item(cursor_row)
        row = content['values']

        if row:
            self.enroll_id.set(row[0])
            self.student_id.set(row[1])
            self.course_id.set(row[2])
            self.pre_requisite.set(row[3])
