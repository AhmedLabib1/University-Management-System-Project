from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class StudentManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.student_id = StringVar()
        self.national_id = StringVar()
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.phone_number = StringVar()
        self.email = StringVar()
        self.gpa = StringVar()
        self.department_id = StringVar()
        self.year = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Student Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=230)

        # Labels and Entry fields
        Label(form_frame, text="Student ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        self.entry_id = ttk.Entry(form_frame, textvariable=self.student_id, font=('Arial', 12), width=25, state='disabled')
        self.entry_id.grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="National ID", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.national_id, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="First Name", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.first_name, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Last Name", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.last_name, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Label(form_frame, text="Phone Number", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.phone_number, font=('Arial', 12), width=25).grid(row=2, column=1, padx=10, pady=5)

        Label(form_frame, text="Email", font=('Arial', 12)).grid(row=2, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.email, font=('Arial', 12), width=25).grid(row=2, column=3, padx=10, pady=5)

        Label(form_frame, text="GPA", font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.gpa, font=('Arial', 12), width=25).grid(row=3, column=1, padx=10, pady=5)

        Label(form_frame, text="Department ID", font=('Arial', 12)).grid(row=3, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.department_id, font=('Arial', 12), width=25).grid(row=3, column=3, padx=10, pady=5)

        Label(form_frame, text="Year", font=('Arial', 12)).grid(row=4, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.year, font=('Arial', 12), width=25).grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        Button(form_frame, text="Add", command=self.add_student, font=('Arial', 12), bg='green', fg='white').grid(row=5, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_student, font=('Arial', 12), bg='blue', fg='white').grid(row=5, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_student, font=('Arial', 12), bg='red', fg='white').grid(row=5, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=5, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=290, width=780, height=290)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("ID", "National_ID", "First_Name", "Last_Name", "Phone", "Email", "GPA", "Dept_ID", "Year"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Setting headings manually
        self.student_table.heading("ID", text="Student ID")
        self.student_table.heading("National_ID", text="National ID")
        self.student_table.heading("First_Name", text="First Name")
        self.student_table.heading("Last_Name", text="Last Name")
        self.student_table.heading("Phone", text="Phone Number")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("GPA", text="GPA")
        self.student_table.heading("Dept_ID", text="Department ID")
        self.student_table.heading("Year", text="Year")

        # Setting column properties manually
        self.student_table.column("ID", width=100, anchor=CENTER)
        self.student_table.column("National_ID", width=100, anchor=CENTER)
        self.student_table.column("First_Name", width=150, anchor=CENTER)
        self.student_table.column("Last_Name", width=150, anchor=CENTER)
        self.student_table.column("Phone", width=100, anchor=CENTER)
        self.student_table.column("Email", width=150, anchor=CENTER)
        self.student_table.column("GPA", width=50, anchor=CENTER)
        self.student_table.column("Dept_ID", width=100, anchor=CENTER)
        self.student_table.column("Year", width=50, anchor=CENTER)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_students()

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

    def fetch_students(self):
        # Clear current table rows
        self.student_table.delete(*self.student_table.get_children())
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Student_ID, national_ID, first_name, last_name, phone_number, Email, GPA, department_id, year FROM students")
                rows = cursor.fetchall()
                for row in rows:
                    # Replace None values with empty strings for clean display
                    clean_row = [val if val is not None else "" for val in row]
                    self.student_table.insert("", END, values=clean_row)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching students: {str(e)}")

    def add_student(self):
        if not self.first_name.get() or not self.last_name.get() or not self.national_id.get() or not self.department_id.get():
            messagebox.showerror("Error", "All fields must be filled out!")
            return
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (national_ID, first_name, last_name, phone_number, Email, GPA, department_id, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (self.national_id.get(), self.first_name.get(), self.last_name.get(), self.phone_number.get(),
                    self.email.get(), self.gpa.get(), self.department_id.get(), self.year.get())
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student added successfully!")
                self.fetch_students()
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding student: {str(e)}")

    def update_student(self):
        if not self.student_id.get():
            messagebox.showerror("Error", "No student selected for updating!")
            return
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE students SET national_ID=?, first_name=?, last_name=?, phone_number=?, Email=?, GPA=?, department_id=?, year=? WHERE Student_ID=?",
                    (self.national_id.get(), self.first_name.get(), self.last_name.get(), self.phone_number.get(),
                    self.email.get(), self.gpa.get(), self.department_id.get(), self.year.get(), self.student_id.get())
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student updated successfully!")
                self.fetch_students()
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating student: {str(e)}")

    def delete_student(self):
        if not self.student_id.get():
            messagebox.showerror("Error", "No student selected for deletion!")
            return
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE Student_ID=?", (self.student_id.get(),))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.fetch_students()
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting student: {str(e)}")

    def clear_fields(self):
        self.student_id.set("")
        self.national_id.set("")
        self.first_name.set("")
        self.last_name.set("")
        self.phone_number.set("")
        self.email.set("")
        self.gpa.set("")
        self.department_id.set("")
        self.year.set("")

    def get_cursor(self, event):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content['values']

        if row:
            self.student_id.set(row[0])
            self.national_id.set(row[1])
            self.first_name.set(row[2])
            self.last_name.set(row[3])
            self.phone_number.set(row[4])
            self.email.set(row[5])
            self.gpa.set(row[6])
            self.department_id.set(row[7])
            self.year.set(row[8])
