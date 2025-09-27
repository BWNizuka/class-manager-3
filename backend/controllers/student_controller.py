from fastapi import APIRouter, HTTPException
from backend.models.student import Student

router = APIRouter()
students_db = []

@router.get("/")
def get_students():
    return students_db

@router.post("/")
def create_student(student: Student):
    students_db.append(student)
    return student

@router.get("/{student_id}")
def get_student(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
