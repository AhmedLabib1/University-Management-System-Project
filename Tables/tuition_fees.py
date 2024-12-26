from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class FeesManagement:
    def __init__(self, root):
        self.root = root

        # ================================ Variables ================================
        self.invoice_id = StringVar()
        self.fees = StringVar()
        self.payment_method = StringVar()
        self.paid = StringVar()
        self.student_id = StringVar()

        # ================================ Title ================================
        label_title = Label(self.root, text="Tuition Fees Management", font=('Arial', 20, 'bold'), bg='#0D47A1', fg='white')
        label_title.pack(side=TOP, fill=X)

        # ================================ Form ================================
        form_frame = Frame(self.root, bd=5, relief=RIDGE)
        form_frame.place(x=10, y=50, width=780, height=170)

        Label(form_frame, text="Invoice ID", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.invoice_id, font=('Arial', 12), width=25, state='disabled').grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Fees", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.fees, font=('Arial', 12), width=25).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Payment Method", font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5)
        payment_methods = ["Cash", "Credit Card", "Bank Transfer"]
        payment_method_combobox = ttk.Combobox(form_frame, textvariable=self.payment_method, font=('Arial', 12), width=25, values=payment_methods, state="readonly")
        payment_method_combobox.grid(row=0, column=3, padx=10, pady=5)
        payment_method_combobox.current(0)

        Label(form_frame, text="Paid (T/F)", font=('Arial', 12)).grid(row=1, column=2, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.paid, font=('Arial', 12), width=25).grid(row=1, column=3, padx=10, pady=5)

        Label(form_frame, text="Student ID", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.student_id, font=('Arial', 12), width=25).grid(row=2, column=1, padx=10, pady=5)

        Button(form_frame, text="Add", command=self.add_fee, font=('Arial', 12), bg='green', fg='white').grid(row=3, column=0, padx=10, pady=5)
        Button(form_frame, text="Update", command=self.update_fee, font=('Arial', 12), bg='blue', fg='white').grid(row=3, column=1, padx=10, pady=5)
        Button(form_frame, text="Delete", command=self.delete_fee, font=('Arial', 12), bg='red', fg='white').grid(row=3, column=2, padx=10, pady=5)
        Button(form_frame, text="Clear", command=self.clear_fields, font=('Arial', 12), bg='gray', fg='white').grid(row=3, column=3, padx=10, pady=5)

        # ================================ Table ================================
        table_frame = Frame(self.root, bd=5, relief=RIDGE)
        table_frame.place(x=10, y=230, width=780, height=350)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.fees_table = ttk.Treeview(table_frame, columns=("Invoice ID", "Fees", "Payment Method", "Paid", "Student ID"),
                                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.fees_table.xview)
        scroll_y.config(command=self.fees_table.yview)

        self.fees_table.heading("Invoice ID", text="Invoice ID")
        self.fees_table.heading("Fees", text="Fees")
        self.fees_table.heading("Payment Method", text="Payment Method")
        self.fees_table.heading("Paid", text="Paid")
        self.fees_table.heading("Student ID", text="Student ID")

        self.fees_table.column("Invoice ID", width=100, anchor=CENTER)
        self.fees_table.column("Fees", width=150, anchor=CENTER)
        self.fees_table.column("Payment Method", width=150, anchor=CENTER)
        self.fees_table.column("Paid", width=100, anchor=CENTER)
        self.fees_table.column("Student ID", width=100, anchor=CENTER)

        self.fees_table['show'] = 'headings'
        self.fees_table.pack(fill=BOTH, expand=1)
        self.fees_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_fees()

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

    def fetch_fees(self):
        self.fees_table.delete(*self.fees_table.get_children())
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT invoice_id, fees, payment_method, paid, Student_ID FROM tuition_fees")
            rows = cursor.fetchall()
            for row in rows:
                clean_row = [val if val is not None else "" for val in row]
                self.fees_table.insert('', END, values=clean_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching fees: {str(e)}")

    def add_fee(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tuition_fees (fees, payment_method, paid, Student_ID) VALUES (?, ?, ?, ?)",
                           (self.fees.get(), self.payment_method.get(), self.paid.get(), self.student_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Fee added successfully!")
            self.fetch_fees()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding fee: {str(e)}")

    def update_fee(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE tuition_fees SET fees=?, payment_method=?, paid=? WHERE invoice_id=?",
                           (self.fees.get(), self.payment_method.get(), self.paid.get(), self.invoice_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Fee updated successfully!")
            self.fetch_fees()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating fee: {str(e)}")

    def delete_fee(self):
        try:
            # Get selected row's invoice_id directly from the table
            selected_row = self.fees_table.focus()
            row_data = self.fees_table.item(selected_row, "values")

            if not row_data:
                messagebox.showwarning("Warning", "Please select a record to delete.")
                return
            
            invoice_id_to_delete = row_data[0]  # Assuming Invoice ID is the first column
            
            # Execute delete query
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tuition_fees WHERE invoice_id=?", (invoice_id_to_delete,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Fee deleted successfully!")
            self.fetch_fees()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting fee: {str(e)}")

    def clear_fields(self):
        self.invoice_id.set("")
        self.fees.set("")
        self.payment_method.set("")
        self.paid.set("")
        self.student_id.set("")

    def get_cursor(self, event):
        cursor_row = self.fees_table.focus()
        content = self.fees_table.item(cursor_row)
        row = content['values']

        if row:
            self.invoice_id.set(row[0])
            self.fees.set(row[1])
            self.payment_method.set(row[2])
            self.paid.set(row[3])
            self.student_id.set(row[4])
