from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def create_table():
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Add Student
@app.route("/add", methods=["GET", "POST"])
def add_student():
                                  
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = r;equest.form["course"]
        phone = request.form["phone"]

        conn = sqlite3.connect("student.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO students(name, age, course, phone) VALUES (?, ?, ?, ?)",
            (name, age, course, phone)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    return render_template("add_student.html")


# View Students
@app.route("/students")
def students():

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("students.html", students=students)


# Search Student
@app.route("/search", methods=["GET", "POST"])
def search():

    result = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        conn = sqlite3.connect("student.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + keyword + '%',)
        )

        result = cur.fetchall()

        conn.close()

    return render_template("search.html", students=result)


# Edit Student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        phone = request.form["phone"]

        cur.execute("""
        UPDATE students
        SET name=?, age=?, course=?, phone=?
        WHERE id=?
        """, (name, age, course, phone, id))

        conn.commit()
        conn.close()

        return redirect("/students")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


# Delete Student
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/students")


if __name__ == "__main__":
    app.run(debug=True)