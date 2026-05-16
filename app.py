from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Data storage
students = []
student_id_counter = 1

class Student:
    def __init__(self, name, roll_no, course, email, phone):
        global student_id_counter
        self.id = student_id_counter
        self.name = name
        self.roll_no = roll_no
        self.course = course
        self.email = email
        self.phone = phone
        self.join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student_id_counter += 1

@app.route("/", methods=["GET", "POST"])
def home():
    global students
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        course = request.form.get("course", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        
        # Validation
        if not name:
            flash("Student name is required!", "error")
            return redirect(url_for("home"))
        
        if not roll_no:
            flash("Roll number is required!", "error")
            return redirect(url_for("home"))
        
        # Check for duplicate roll number
        for student in students:
            if student.roll_no == roll_no:
                flash(f"Student with Roll No {roll_no} already exists!", "error")
                return redirect(url_for("home"))
        
        # Create new student
        new_student = Student(name, roll_no, course, email, phone)
        students.append(new_student)
        
        flash(f"Student {name} added successfully!", "success")
        return redirect(url_for("home"))
    
    return render_template("index.html", students=students)

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    global students
    students = [s for s in students if s.id != student_id]
    flash("Student deleted successfully!", "success")
    return redirect(url_for("home"))

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    global students
    student = next((s for s in students if s.id == student_id), None)
    
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        student.name = request.form.get("name", "").strip()
        student.roll_no = request.form.get("roll_no", "").strip()
        student.course = request.form.get("course", "").strip()
        student.email = request.form.get("email", "").strip()
        student.phone = request.form.get("phone", "").strip()
        
        flash("Student updated successfully!", "success")
        return redirect(url_for("home"))
    
    return render_template("edit.html", student=student)

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    if query:
        results = [s for s in students if query in s.name.lower() or query in s.roll_no.lower()]
    else:
        results = students
    return render_template("index.html", students=results, search_query=query)

@app.route("/api/students")
def api_students():
    students_data = [{
        "id": s.id,
        "name": s.name,
        "roll_no": s.roll_no,
        "course": s.course,
        "email": s.email,
        "phone": s.phone,
        "join_date": s.join_date
    } for s in students]
    return jsonify(students_data)

@app.route("/stats")
def stats():
    total_students = len(students)
    courses = {}
    for student in students:
        if student.course:
            courses[student.course] = courses.get(student.course, 0) + 1
    
    return jsonify({
        "total": total_students,
        "courses": courses
    })

if __name__ == "__main__":
    # Add sample data
    if not students:
        students.append(Student("John Doe", "2024001", "Computer Science", "john@example.com", "1234567890"))
        students.append(Student("Jane Smith", "2024002", "Information Technology", "jane@example.com", "0987654321"))
    
    print("🚀 Student Management System Started!")
    print("📱 Access at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)