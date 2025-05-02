from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

app = FastAPI()

# Database connection function
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dor3220fai?",  # Update if you have a password
        database="student_portal"
    )

# Pydantic models
class Student(BaseModel):
    name: str
    email: str

class Course(BaseModel):
    title: str
    instructor: str

class Enrollment(BaseModel):
    student_id: int
    course_id: int

# ===== Students =====
@app.post("/students/", response_model=dict)
def create_student(student: Student):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (student.name, student.email))
        db.commit()
        return {"message": "Student created successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/students/", response_model=List[dict])
def get_students():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return students

@app.put("/students/{student_id}", response_model=dict)
def update_student(student_id: int, student: Student):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE students SET name = %s, email = %s WHERE student_id = %s", (student.name, student.email, student_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student updated successfully"}
    finally:
        cursor.close()
        db.close()

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    finally:
        cursor.close()
        db.close()

# ===== Courses =====
@app.post("/courses/", response_model=dict)
def create_course(course: Course):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO courses (title, instructor) VALUES (%s, %s)", (course.title, course.instructor))
        db.commit()
        return {"message": "Course created successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/courses/", response_model=List[dict])
def get_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return courses

@app.put("/courses/{course_id}", response_model=dict)
def update_course(course_id: int, course: Course):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE courses SET title = %s, instructor = %s WHERE course_id = %s", (course.title, course.instructor, course_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"message": "Course updated successfully"}
    finally:
        cursor.close()
        db.close()

@app.delete("/courses/{course_id}", response_model=dict)
def delete_course(course_id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"message": "Course deleted successfully"}
    finally:
        cursor.close()
        db.close()

# ===== Enrollments =====
@app.post("/enrollments/", response_model=dict)
def create_enrollment(enrollment: Enrollment):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (enrollment.student_id, enrollment.course_id))
        db.commit()
        return {"message": "Enrollment created successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/enrollments/", response_model=List[dict])
def get_enrollments():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.enrollment_id, s.name AS student_name, c.title AS course_title
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
    """)
    enrollments = cursor.fetchall()
    cursor.close()
    db.close()
    return enrollments

@app.put("/enrollments/{enrollment_id}", response_model=dict)
def update_enrollment(enrollment_id: int, enrollment: Enrollment):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE enrollments SET student_id = %s, course_id = %s WHERE enrollment_id = %s", (enrollment.student_id, enrollment.course_id, enrollment_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        return {"message": "Enrollment updated successfully"}
    finally:
        cursor.close()
        db.close()

@app.delete("/enrollments/{enrollment_id}", response_model=dict)
def delete_enrollment(enrollment_id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM enrollments WHERE enrollment_id = %s", (enrollment_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        return {"message": "Enrollment deleted successfully"}
    finally:
        cursor.close()
        db.close()