from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class CourseManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.course_id = StringVar()
        self.course_name = StringVar()
        self.credit_hours = StringVar()
        self.department = StringVar()
        self.lecturer = StringVar()
        self.year = StringVar()
        self.room = StringVar()
        self.date = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Course Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=200)

        # Labels and Entry Fields
        ttk.Label(form_frame, text="Course ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_id, font=('Arial', 12), width=25, state=DISABLED).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Course Name", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_name, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="Credit Hours", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.credit_hours, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Department", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.department, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Label(form_frame, text="Lecturer", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.lecturer, font=('Arial', 12), width=25).grid(row=2, column=1, padx=10, pady=5)

        Label(form_frame, text="Year", font=('Arial', 12)).grid(row=2, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.year, font=('Arial', 12), width=25).grid(row=2, column=3, padx=10, pady=5)

        Label(form_frame, text="Room", font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.room, font=('Arial', 12), width=25).grid(row=3, column=1, padx=10, pady=5)

        Label(form_frame, text="Date", font=('Arial', 12)).grid(row=3, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.date, font=('Arial', 12), width=25).grid(row=3, column=3, padx=10, pady=5)

        # Buttons
        Button(form_frame, text="Add", command=self.add_course, font=('Arial', 12), bg='green', fg='white').grid(row=4, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_course, font=('Arial', 12), bg='blue', fg='white').grid(row=4, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_course, font=('Arial', 12), bg='red', fg='white').grid(row=4, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=4, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=260, width=780, height=320)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.course_table = ttk.Treeview(
            table_frame,
            columns=("course_ID", "course_name", "credit_hours", "lecturer", "department", "year", "room", "date"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.course_table.xview)
        scroll_y.config(command=self.course_table.yview)

        # Table Headings
        self.course_table.heading("course_ID", text="Course ID")
        self.course_table.heading("course_name", text="Name")
        self.course_table.heading("credit_hours", text="Credit Hours")
        self.course_table.heading("lecturer", text="Lecturer")
        self.course_table.heading("department", text="Department")
        self.course_table.heading("year", text="Year")
        self.course_table.heading("room", text="Room")
        self.course_table.heading("date", text="Date")

        # Column Widths
        self.course_table.column("course_ID", width=70, anchor=CENTER)
        self.course_table.column("course_name", width=120, anchor=CENTER)
        self.course_table.column("credit_hours", width=70, anchor=CENTER)
        self.course_table.column("lecturer", width=100, anchor=CENTER)
        self.course_table.column("department", width=100, anchor=CENTER)
        self.course_table.column("year", width=70, anchor=CENTER)
        self.course_table.column("room", width=70, anchor=CENTER)
        self.course_table.column("date", width=100, anchor=CENTER)

        self.course_table["show"] = "headings"
        self.course_table.pack(fill=BOTH, expand=1)
        self.course_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_courses()

    # ================================ Database Operations ================================
    
    def connect_db(self):
        try:
            # Update connection string to use SQL Server
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
        
    def fetch_courses(self):
        # Clear the table first
        self.course_table.delete(*self.course_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")  # Fetch all rows
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    # Handle None values (e.g., replace None with empty string)
                    clean_row = [val if val is not None else "" for val in row]
                    self.course_table.insert("", END, values=clean_row)
            else:
                messagebox.showinfo("Info", "No data found in the database.")
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching courses: {str(e)}")

    def add_course(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO courses (course_name, credit_hours, lecturer, department, year, room, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    self.course_name.get(),
                    self.credit_hours.get(),
                    self.lecturer.get(),
                    self.department.get(),
                    self.year.get(),
                    self.room.get(),
                    self.date.get(),
                ),
            )
            conn.commit() # Saves the changes
            conn.close()  # Closes the database connection
            
            messagebox.showinfo("Success", "Course added successfully!")
            self.fetch_courses()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding course: {str(e)}")

    def update_course(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE courses SET course_name=?, credit_hours=?, lecturer=?, department=?, year=?, room=?, date=? WHERE course_ID=?",
                (
                    self.course_name.get(),
                    self.credit_hours.get(),
                    self.lecturer.get(),
                    self.department.get(),
                    self.year.get(),
                    self.room.get(),
                    self.date.get(),
                    self.course_id.get(),
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Course updated successfully!")
            self.fetch_courses()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating course: {str(e)}")

    def delete_course(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM courses WHERE course_ID=?", (self.course_id.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Course deleted successfully!")
            self.fetch_courses()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting course: {str(e)}")

    def clear_fields(self):
        self.course_id.set("")
        self.course_name.set("")
        self.credit_hours.set("")
        self.department.set("")
        self.lecturer.set("")
        self.year.set("")
        self.room.set("")
        self.date.set("")

    def get_cursor(self, event):
        cursor_row = self.course_table.focus()
        content = self.course_table.item(cursor_row)
        row = content['values']

        self.course_id.set(row[0])
        self.course_name.set(row[1])
        self.credit_hours.set(row[2])
        self.lecturer.set(row[3])
        self.department.set(row[4])
        self.year.set(row[5])
        self.room.set(row[6])
        self.date.set(row[7])
