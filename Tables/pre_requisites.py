from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class PreRequisitesManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.course_id = StringVar()
        self.pre_requisite_id = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Pre-Requisites Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=100)

        Label(form_frame, text="Course ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_id, font=('Arial', 12), width=25).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Pre-Requisite ID", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.pre_requisite_id, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_pre_requisite, font=('Arial', 12), bg='green', fg='white').grid(row=1, column=0, padx=10, pady=15)
        Button(form_frame, text="Update", command=self.update_pre_requisite, font=('Arial', 12), bg='blue', fg='white').grid(row=1, column=1, padx=10, pady=15)
        Button(form_frame, text="Delete", command=self.delete_pre_requisite, font=('Arial', 12), bg='red', fg='white').grid(row=1, column=2, padx=10, pady=15)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=1, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=160, width=780, height=420)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.pre_requisites_table = ttk.Treeview(
            table_frame,
            columns=("Course ID", "Pre-Requisite ID"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.pre_requisites_table.xview)
        scroll_y.config(command=self.pre_requisites_table.yview)

        self.pre_requisites_table.heading("Course ID", text="Course ID")
        self.pre_requisites_table.heading("Pre-Requisite ID", text="Pre-Requisite ID")

        self.pre_requisites_table.column("Course ID", width=200, anchor=CENTER)
        self.pre_requisites_table.column("Pre-Requisite ID", width=200, anchor=CENTER)

        self.pre_requisites_table['show'] = 'headings'
        self.pre_requisites_table.pack(fill=BOTH, expand=1)
        self.pre_requisites_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_pre_requisites()

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

    def fetch_pre_requisites(self):
        self.pre_requisites_table.delete(*self.pre_requisites_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pre_requisites")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.pre_requisites_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching pre-requisites: {str(e)}")

    def add_pre_requisite(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pre_requisites (course_ID, pre_requisite_id) VALUES (?, ?)",
                           (self.course_id.get(), self.pre_requisite_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Pre-Requisite added successfully!")
            self.fetch_pre_requisites()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding pre-requisite: {str(e)}")

    def update_pre_requisite(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE pre_requisites SET pre_requisite_id=? WHERE course_ID=?",
                           (self.pre_requisite_id.get(), self.course_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Pre-Requisite updated successfully!")
            self.fetch_pre_requisites()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating pre-requisite: {str(e)}")

    def delete_pre_requisite(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pre_requisites WHERE course_ID=? AND pre_requisite_id=?",
                           (self.course_id.get(), self.pre_requisite_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Pre-Requisite deleted successfully!")
            self.fetch_pre_requisites()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting pre-requisite: {str(e)}")

    def clear_fields(self):
        self.course_id.set("")
        self.pre_requisite_id.set("")

    def get_cursor(self, event):
        cursor_row = self.pre_requisites_table.focus()
        content = self.pre_requisites_table.item(cursor_row)
        row = content['values']

        if row:
            self.course_id.set(row[0])
            self.pre_requisite_id.set(row[1])