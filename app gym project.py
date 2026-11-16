
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

conn = sqlite3.connect("gym_progress.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_date TEXT,
    exercise TEXT,
    weight REAL,
    sets INTEGER,
    reps INTEGER
)
""")
conn.commit()


def add_workout():
    exercise = exercise_entry.get()
    weight = weight_entry.get()
    sets = sets_entry.get()
    reps = reps_entry.get()

    if not exercise or not weight or not sets or not reps:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        weight = float(weight)
        sets = int(sets)
        reps = int(reps)

        if weight < 0 or sets <= 0 or reps <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Error", "Enter valid workout values")
        return

    cursor.execute("""
    INSERT INTO workouts (workout_date, exercise, weight, sets, reps)
    VALUES (?, ?, ?, ?, ?)
    """, (date.today().isoformat(), exercise, weight, sets, reps))

    conn.commit()

    messagebox.showinfo("Success", "Workout added successfully")

    exercise_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    sets_entry.delete(0, tk.END)
    reps_entry.delete(0, tk.END)

    view_workouts()


def view_workouts():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM workouts ORDER BY id DESC")
    records = cursor.fetchall()

    for record in records:
        tree.insert("", tk.END, values=record)

    total_label.config(text=f"Total Workouts: {len(records)}")


def delete_workout():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a workout to delete")
        return

    workout_id = tree.item(selected[0])["values"][0]

    cursor.execute("DELETE FROM workouts WHERE id=?", (workout_id,))
    conn.commit()

    messagebox.showinfo("Success", "Workout deleted")
    view_workouts()


root = tk.Tk()
root.title("Gym Progress Tracker")
root.geometry("850x600")
root.configure(bg="#20242c")

title = tk.Label(
    root,
    text="GYM PROGRESS TRACKER",
    font=("Arial", 22, "bold"),
    bg="#20242c",
    fg="white"
)
title.pack(pady=20)

form = tk.Frame(root, bg="#303641", padx=20, pady=15)
form.pack(pady=10)

def create_field(label, row):
    tk.Label(
        form,
        text=label,
        font=("Arial", 11),
        bg="#303641",
        fg="white"
    ).grid(row=row, column=0, padx=10, pady=8, sticky="w")

    entry = tk.Entry(form, font=("Arial", 11), width=25)
    entry.grid(row=row, column=1, padx=10, pady=8)
    return entry


exercise_entry = create_field("Exercise Name:", 0)
weight_entry = create_field("Weight (kg):", 1)
sets_entry = create_field("Number of Sets:", 2)
reps_entry = create_field("Repetitions:", 3)

tk.Button(
    form,
    text="Add Workout",
    command=add_workout,
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
).grid(row=4, column=0, columnspan=2, pady=12)

total_label = tk.Label(
    root,
    text="Total Workouts: 0",
    font=("Arial", 12, "bold"),
    bg="#20242c",
    fg="#f1c40f"
)
total_label.pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack(padx=20, pady=10, fill="both", expand=True)

columns = ("ID", "Date", "Exercise", "Weight", "Sets", "Reps")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack(fill="both", expand=True)

tk.Button(
    root,
    text="Delete Selected Workout",
    command=delete_workout,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold")
).pack(pady=10)

view_workouts()

root.mainloop()
