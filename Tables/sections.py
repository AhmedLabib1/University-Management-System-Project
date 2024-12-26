from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class SectionsManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.course_id = StringVar()
        self.dr_id = StringVar()
        self.assistant_id = StringVar()
        self.date = StringVar()
        self.room = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Sections Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=165)

        Label(form_frame, text="Course ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_id, font=('Arial', 12), width=25).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Lecturer ID", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.dr_id, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Assistant ID", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.assistant_id, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="Date", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.date, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Label(form_frame, text="Room", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.room, font=('Arial', 12), width=25).grid(row=2, column=1, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_section, font=('Arial', 12), bg='green', fg='white').grid(row=3, column=0, padx=10, pady=15)
        Button(form_frame, text="Update", command=self.update_section, font=('Arial', 12), bg='blue', fg='white').grid(row=3, column=1, padx=10, pady=15)
        Button(form_frame, text="Delete", command=self.delete_section, font=('Arial', 12), bg='red', fg='white').grid(row=3, column=2, padx=10, pady=15)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=3, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=225, width=780, height=355)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.section_table = ttk.Treeview(
            table_frame,
            columns=("Course ID", "Lecturer ID", "Assistant ID", "Date", "Room"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.section_table.xview)
        scroll_y.config(command=self.section_table.yview)

        self.section_table.heading("Course ID", text="Course ID")
        self.section_table.heading("Lecturer ID", text="Lecturer ID")
        self.section_table.heading("Assistant ID", text="Assistant ID")
        self.section_table.heading("Date", text="Date")
        self.section_table.heading("Room", text="Room")

        self.section_table.column("Course ID", width=200, anchor=CENTER)
        self.section_table.column("Lecturer ID", width=200, anchor=CENTER)
        self.section_table.column("Assistant ID", width=200, anchor=CENTER)
        self.section_table.column("Date", width=150, anchor=CENTER)
        self.section_table.column("Room", width=100, anchor=CENTER)

        self.section_table['show'] = 'headings'
        self.section_table.pack(fill=BOTH, expand=1)
        self.section_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_sections()

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

    def fetch_sections(self):
        self.section_table.delete(*self.section_table.get_children())  # Clears the table

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            # Correct SQL query to fetch data from the sections table
            cursor.execute("SELECT course_ID, dr_ID, assistant_ID, date, room FROM sections")

            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]  # Replace None with empty string
                self.section_table.insert('', END, values=clean_row)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching sections: {str(e)}")

    def add_section(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sections (course_ID, dr_ID, assistant_ID, date, room)
                VALUES (?, ?, ?, ?, ?)
            """, (self.course_id.get(), self.dr_id.get(), self.assistant_id.get(), self.date.get(), self.room.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Section added successfully!")
            self.fetch_sections()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding section: {str(e)}")

    def update_section(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE sections
                SET date=?, room=?
                WHERE course_ID=? AND dr_ID=? AND assistant_ID=?
            """, (self.date.get(), self.room.get(), self.course_id.get(), self.dr_id.get(), self.assistant_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Section updated successfully!")
            self.fetch_sections()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating section: {str(e)}")

    def delete_section(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM sections
                WHERE course_ID=? AND dr_ID=? AND assistant_ID=?
            """, (self.course_id.get(), self.dr_id.get(), self.assistant_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Section deleted successfully!")
            self.fetch_sections()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting section: {str(e)}")

    def clear_fields(self):
        self.course_id.set("")
        self.dr_id.set("")
        self.assistant_id.set("")
        self.date.set("")
        self.room.set("")

    def get_cursor(self, event):
        cursor_row = self.section_table.focus()
        content = self.section_table.item(cursor_row)
        row = content['values']

        if row:
            self.course_id.set(row[0])
            self.dr_id.set(row[1])
            self.assistant_id.set(row[2])
            self.date.set(row[3])
            self.room.set(row[4])
