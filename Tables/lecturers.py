from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class LecturerManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.dr_id = StringVar()
        self.national_id = StringVar()
        self.name = StringVar()
        self.salary = StringVar()
        self.department_id = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Lecturer Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=165)

        Label(form_frame, text="Lecturer ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.dr_id, font=('Arial', 12), width=25, state=DISABLED).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="National ID", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.national_id, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Name", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.name, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="Salary", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.salary, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Label(form_frame, text="Department ID", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.department_id, font=('Arial', 12), width=25).grid(row=2, column=1, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_lecturer, font=('Arial', 12), bg='green', fg='white').grid(row=3, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_lecturer, font=('Arial', 12), bg='blue', fg='white').grid(row=3, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_lecturer, font=('Arial', 12), bg='red', fg='white').grid(row=3, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=3, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=225, width=780, height=355)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.lecturer_table = ttk.Treeview(
            table_frame,
            columns=("Lecturer ID", "National ID", "Name", "Salary", "Department ID"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.lecturer_table.xview)
        scroll_y.config(command=self.lecturer_table.yview)

        self.lecturer_table.heading("Lecturer ID", text="Lecturer ID")
        self.lecturer_table.heading("National ID", text="National ID")
        self.lecturer_table.heading("Name", text="Name")
        self.lecturer_table.heading("Salary", text="Salary")
        self.lecturer_table.heading("Department ID", text="Department ID")

        self.lecturer_table.column("Lecturer ID", width=100, anchor=CENTER)
        self.lecturer_table.column("National ID", width=150, anchor=CENTER)
        self.lecturer_table.column("Name", width=200, anchor=CENTER)
        self.lecturer_table.column("Salary", width=100, anchor=CENTER)
        self.lecturer_table.column("Department ID", width=100, anchor=CENTER)

        self.lecturer_table['show'] = 'headings'
        self.lecturer_table.pack(fill=BOTH, expand=1)
        self.lecturer_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_lecturers()

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

    def fetch_lecturers(self):
        self.lecturer_table.delete(*self.lecturer_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lecturers")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.lecturer_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching lecturers: {str(e)}")

    def add_lecturer(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lecturers (national_ID, name, salary, department_id) VALUES (?, ?, ?, ?)",
                           (self.national_id.get(), self.name.get(), self.salary.get(), self.department_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lecturer added successfully!")
            self.fetch_lecturers()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding lecturer: {str(e)}")

    def update_lecturer(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE lecturers SET national_ID=?, name=?, salary=?, department_id=? WHERE dr_ID=?",
                           (self.national_id.get(), self.name.get(), self.salary.get(), self.department_id.get(), self.dr_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lecturer updated successfully!")
            self.fetch_lecturers()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating lecturer: {str(e)}")

    def delete_lecturer(self):
        try:
            dr_id_to_delete = self.dr_id.get()
            if not dr_id_to_delete:
                messagebox.showwarning("Warning", "Please enter a valid Lecturer ID.")
                return

            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lecturers WHERE dr_ID=?", (dr_id_to_delete,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Lecturer deleted successfully!")
            self.fetch_lecturers()
            self.clear_fields()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting lecturer: {str(e)}")


    def clear_fields(self):
        self.dr_id.set("")
        self.national_id.set("")
        self.name.set("")
        self.salary.set("")
        self.department_id.set("")

    def get_cursor(self, event):
        cursor_row = self.lecturer_table.focus()
        content = self.lecturer_table.item(cursor_row)
        row = content['values']

        if row:
            self.dr_id.set(row[0])
            self.national_id.set(row[1])
            self.name.set(row[2])
            self.salary.set(row[3])
            self.department_id.set(row[4])
