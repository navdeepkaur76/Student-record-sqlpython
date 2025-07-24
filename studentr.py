from tkinter import *
from tkinter import messagebox
import pymysql

# ========== DATABASE SETUP ========== #
def create_table():
    try:
        conn = pymysql.connect(host="localhost", user="root", password="", db="school")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            NAME VARCHAR(100),
            ROLLNO VARCHAR(20) PRIMARY KEY,
            COURSE VARCHAR(100),
            MATH FLOAT,
            SCIENCE FLOAT,
            ENGLISH FLOAT,
            TOTAL FLOAT,
            PERCENTAGE FLOAT,
            GRADE VARCHAR(10)
        )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating table:\n{e}")

# ========== CORE FUNCTIONS ========== #
def clear_fields():
    for entry in [e1, e2, e3, e4, e5, e6, e7, e8, e9]:
        entry.delete(0, END)

def calculate():
    try:
        math = float(e4.get())
        science = float(e5.get())
        english = float(e6.get())

        total = math + science + english
        percentage = (total / 300) * 100

        if percentage > 80:
            grade = "Grade-A"
        elif percentage >= 60:
            grade = "Grade-B"
        elif percentage >= 40:
            grade = "Grade-C"
        else:
            grade = "Grade-F"

        e7.delete(0, END)
        e8.delete(0, END)
        e9.delete(0, END)
        e7.insert(0, total)
        e8.insert(0, percentage)
        e9.insert(0, grade)
    except:
        messagebox.showerror("Error", "Please enter valid marks.")

def add_record():
    try:
        calculate()
        name = e1.get()
        roll = e2.get()
        course = e3.get()
        math = float(e4.get())
        science = float(e5.get())
        english = float(e6.get())
        total = float(e7.get())
        percentage = float(e8.get())
        grade = e9.get()

        conn = pymysql.connect(host="localhost", user="root", password="", db="school")
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO students 
        (NAME, ROLLNO, COURSE, MATH, SCIENCE, ENGLISH, TOTAL, PERCENTAGE, GRADE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, roll, course, math, science, english, total, percentage, grade))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record added successfully!")
    except pymysql.err.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add record\n{e}")

def search_record():
    try:
        name = e1.get()
        roll = e2.get()
        course = e3.get()

        conn = pymysql.connect(host="localhost", user="root", password="", db="school")
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM students 
        WHERE NAME = %s OR ROLLNO = %s OR COURSE = %s
        LIMIT 1
        """, (name, roll, course))
        result = cur.fetchone()
        conn.close()

        if result:
            for idx, entry in enumerate([e1, e2, e3, e4, e5, e6, e7, e8, e9]):
                entry.delete(0, END)
                entry.insert(0, result[idx])
        else:
            messagebox.showinfo("Not Found", "No matching record found.")
    except Exception as e:
        messagebox.showerror("Error", f"Search failed\n{e}")

def update_record():
    try:
        calculate()
        name = e1.get()
        roll = e2.get()
        course = e3.get()
        math = float(e4.get())
        science = float(e5.get())
        english = float(e6.get())
        total = float(e7.get())
        percentage = float(e8.get())
        grade = e9.get()

        conn = pymysql.connect(host="localhost", user="root", password="", db="school")
        cur = conn.cursor()
        cur.execute("""
        UPDATE students SET 
        NAME=%s, COURSE=%s, MATH=%s, SCIENCE=%s, ENGLISH=%s, 
        TOTAL=%s, PERCENTAGE=%s, GRADE=%s 
        WHERE ROLLNO=%s
        """, (name, course, math, science, english, total, percentage, grade, roll))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Update failed\n{e}")

def delete_record():
    try:
        roll = e2.get()
        conn = pymysql.connect(host="localhost", user="root", password="", db="school")
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE ROLLNO = %s", (roll,))
        conn.commit()
        conn.close()
        clear_fields()
        messagebox.showinfo("Deleted", "Record deleted (if existed).")
    except:
        messagebox.showerror("Error", "Failed to delete record.")

# ========== GUI SETUP ========== #
master = Tk()
master.title("Student Grade System")
master.configure(bg="#f8f9fa")
master.geometry("600x400")
master.resizable(False, False)

label_font = ("Helvetica", 10, "bold")
entry_font = ("Helvetica", 10)
bg_color = "#f8f9fa"
label_fg = "#2c3e50"
entry_bg = "#ffffff"
entry_fg = "#000000"
button_bg = "#3498db"
button_fg = "white"

# Labels and Entries
labels = ["Name", "Roll No", "Course", "Math", "Science", "English", "Total Marks", "Percentage", "Grade"]
entries = []

for i, text in enumerate(labels):
    Label(master, text=f"{text}:", font=label_font, fg=label_fg, bg=bg_color).grid(row=i, column=0, padx=10, pady=5, sticky=E)
    entry = Entry(master, bg=entry_bg, fg=entry_fg, font=entry_font, width=25)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky=W)
    entries.append(entry)

e1, e2, e3, e4, e5, e6, e7, e8, e9 = entries

# Buttons
Button(master, text="Calculate", command=calculate, bg=button_bg, fg=button_fg, width=15).grid(row=0, column=3, padx=10)
Button(master, text="Add Record", command=add_record, bg=button_bg, fg=button_fg, width=15).grid(row=1, column=3, padx=10)
Button(master, text="Search Record", command=search_record, bg=button_bg, fg=button_fg, width=15).grid(row=2, column=3, padx=10)
Button(master, text="Update Record", command=update_record, bg=button_bg, fg=button_fg, width=15).grid(row=3, column=3, padx=10)
Button(master, text="Delete Record", command=delete_record, bg="#e74c3c", fg="white", width=15).grid(row=4, column=3, padx=10)
Button(master, text="Clear", command=clear_fields, bg="#95a5a6", fg="white", width=15).grid(row=5, column=3, padx=10)
Button(master, text="Exit", command=master.quit, bg="#2ecc71", fg="white", width=15).grid(row=6, column=3, padx=10)

# ========== INIT ========== #
create_table()
mainloop()
