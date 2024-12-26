from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc  # SQL Server uses pyodbc for connection

class DepartmentManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.department_id = StringVar()
        self.department_name = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Department Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=100)

        Label(form_frame, text="Department ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.department_id, font=('Arial', 12), width=25, state=DISABLED).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Department Name", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.department_name, font=('Arial', 12), width=23).grid(row=0, column=3, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_department, font=('Arial', 12), bg='green', fg='white').grid(row=1, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_department, font=('Arial', 12), bg='blue', fg='white').grid(row=1, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_department, font=('Arial', 12), bg='red', fg='white').grid(row=1, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=1, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=160, width=780, height=420)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.department_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.department_table.xview)
        scroll_y.config(command=self.department_table.yview)

        self.department_table.heading("ID", text="Department ID")
        self.department_table.heading("Name", text="Department Name")

        self.department_table.column("ID", width=100, anchor=CENTER)
        self.department_table.column("Name", width=200, anchor=CENTER)

        self.department_table["show"] = "headings"
        self.department_table.pack(fill=BOTH, expand=1)
        self.department_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_departments()

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

    def fetch_departments(self):
        self.department_table.delete(*self.department_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT department_ID, name FROM departments")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.department_table.insert("", END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching departments: {str(e)}")

    def add_department(self):
        if self.department_name.get() == "":
            messagebox.showerror("Error", "Department Name cannot be empty!")
            return
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO departments (name) VALUES (?)", (self.department_name.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Department added successfully!")
            self.fetch_departments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding department: {str(e)}")

    def update_department(self):
        if self.department_id.get() == "":
            messagebox.showerror("Error", "Select a department to update!")
            return
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE departments SET name=? WHERE department_ID=?",
                (self.department_name.get(), self.department_id.get()),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Department updated successfully!")
            self.fetch_departments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating department: {str(e)}")

    def delete_department(self):
        if self.department_id.get() == "":
            messagebox.showerror("Error", "Select a department to delete!")
            return
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departments WHERE department_ID=?", (self.department_id.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Department deleted successfully!")
            self.fetch_departments()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting department: {str(e)}")

    def clear_fields(self):
        self.department_id.set("")  # Clear department ID
        self.department_name.set("")  # Clear department name entry

    def get_cursor(self, event):
        cursor_row = self.department_table.focus()
        content = self.department_table.item(cursor_row)
        row = content['values']

        if row:
            self.department_id.set(row[0])  # Set the department ID
            self.department_name.set(row[1])  # Set the department name