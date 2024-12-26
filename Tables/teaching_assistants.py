from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc  # Use pyodbc to connect to SQL Server

class TeachingAssistantsManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.id = StringVar()
        self.name = StringVar()
        self.salary = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Teaching Assistants Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=130)

        Label(form_frame, text="TA ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.id, font=('Arial', 12), width=25, state=DISABLED).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Name", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.name, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Salary", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.salary, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_ta, font=('Arial', 12), bg='green', fg='white').grid(row=2, column=1, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_ta, font=('Arial', 12), bg='blue', fg='white').grid(row=2, column=2, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_ta, font=('Arial', 12), bg='red', fg='white').grid(row=2, column=3, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=2, column=4, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=190, width=780, height=390)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.ta_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Salary"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.ta_table.xview)
        scroll_y.config(command=self.ta_table.yview)

        self.ta_table.heading("ID", text="ID")
        self.ta_table.heading("Name", text="Name")
        self.ta_table.heading("Salary", text="Salary")

        self.ta_table.column("ID", width=100, anchor=CENTER)
        self.ta_table.column("Name", width=200, anchor=CENTER)
        self.ta_table.column("Salary", width=100, anchor=CENTER)

        self.ta_table['show'] = 'headings'
        self.ta_table.pack(fill=BOTH, expand=1)
        self.ta_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_ta()

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

    def fetch_ta(self):
        self.ta_table.delete(*self.ta_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teaching_assistants")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.ta_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {str(e)}")

    def add_ta(self):
        try:
            conn = self.connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("INSERT INTO teaching_assistants (name, salary) VALUES (?, ?)",
                           (self.name.get(), float(self.salary.get())))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Teaching Assistant added successfully!")
            self.fetch_ta()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding TA: {str(e)}")

    def update_ta(self):
        try:
            # Validate salary is an integer
            salary_value = self.salary.get()
            if not salary_value.isdigit():
                messagebox.showerror("Input Error", "Salary must be a valid integer.")
                return
            
            salary_value = float(salary_value)

            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE teaching_assistants SET name=?, salary=? WHERE ID=?",
                           (self.name.get(), salary_value, self.id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Teaching Assistant updated successfully!")
            self.fetch_ta()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating TA: {str(e)}")

    def delete_ta(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teaching_assistants WHERE ID=?", (self.id.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Teaching Assistant deleted successfully!")
            self.fetch_ta()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting TA: {str(e)}")

    def clear_fields(self):
            self.id.set("")
            self.name.set("")
            self.salary.set("")

    def get_cursor(self, event):
        cursor_row = self.ta_table.focus()
        content = self.ta_table.item(cursor_row)
        row = content['values']

        if row:
            self.id.set(row[0])
            self.name.set(row[1])
            self.salary.set(row[2])

