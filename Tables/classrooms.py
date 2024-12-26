from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class ClassroomManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.room_number = StringVar()
        self.date = StringVar()
        self.capacity = StringVar()
        self.building = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Classroom Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=130)

        Label(form_frame, text="Room Number", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.room_number, font=('Arial', 12), width=25, state=DISABLED).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Date", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.date, font=('Arial', 12), width=25).grid(row=0, column=3, padx=10, pady=5)

        Label(form_frame, text="Capacity", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.capacity, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Building", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.building, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_classroom, font=('Arial', 12), bg='green', fg='white').grid(row=2, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_classroom, font=('Arial', 12), bg='blue', fg='white').grid(row=2, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_classroom, font=('Arial', 12), bg='red', fg='white').grid(row=2, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=2, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=190, width=780, height=390)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.classroom_table = ttk.Treeview(table_frame, columns=("Room Number", "Date", "Capacity", "Building"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.classroom_table.xview)
        scroll_y.config(command=self.classroom_table.yview)

        self.classroom_table.heading("Room Number", text="Room Number")
        self.classroom_table.heading("Date", text="Date")
        self.classroom_table.heading("Capacity", text="Capacity")
        self.classroom_table.heading("Building", text="Building")

        self.classroom_table.column("Room Number", width=100, anchor=CENTER)
        self.classroom_table.column("Date", width=200, anchor=CENTER)
        self.classroom_table.column("Capacity", width=100, anchor=CENTER)
        self.classroom_table.column("Building", width=200, anchor=CENTER)

        self.classroom_table['show'] = 'headings'
        self.classroom_table.pack(fill=BOTH, expand=1)
        self.classroom_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_classrooms()

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

    def fetch_classrooms(self):
        self.classroom_table.delete(*self.classroom_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classrooms")
            rows = cursor.fetchall()

            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.classroom_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching classrooms: {str(e)}")

    def add_classroom(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO classrooms (date, capacity, building) VALUES (?, ?, ?)",
                           (self.date.get(), self.capacity.get(), self.building.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Classroom added successfully!")
            self.fetch_classrooms()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding classroom: {str(e)}")

    def update_classroom(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE classrooms SET date=?, capacity=?, building=? WHERE Room_number=?",
                           (self.date.get(), self.capacity.get(), self.building.get(), self.room_number.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Classroom updated successfully!")
            self.fetch_classrooms()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating classroom: {str(e)}")

    def delete_classroom(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM classrooms WHERE Room_number=?", (self.room_number.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Classroom deleted successfully!")
            self.fetch_classrooms()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting classroom: {str(e)}")

    def clear_fields(self):
        self.room_number.set("")
        self.date.set("")
        self.capacity.set("")
        self.building.set("")

    def get_cursor(self, event):
        cursor_row = self.classroom_table.focus()
        contents = self.classroom_table.item(cursor_row)
        row = contents['values']
        self.room_number.set(row[0])
        self.date.set(row[1])
        self.capacity.set(row[2])
        self.building.set(row[3])
