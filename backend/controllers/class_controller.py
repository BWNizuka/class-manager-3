from fastapi import APIRouter, HTTPException
from backend.models.class import Class
from backend.models.student import Student
from backend.models.teacher import Teacher

router = APIRouter()
classes_db = []

@router.get("/")
def get_classes():
    return classes_db

@router.post("/")
def create_class(cls: Class):
    classes_db.append(cls)
    return cls

@router.post("/{class_id}/add_student")
def add_student_to_class(class_id: int, student: Student):
    for cls in classes_db:
        if cls.id == class_id:
            cls.students.append(student)
            return cls
    raise HTTPException(status_code=404, detail="Class not found")

@router.post("/{class_id}/assign_teacher")
def assign_teacher_to_class(class_id: int, teacher: Teacher):
    for cls in classes_db:
        if cls.id == class_id:
            cls.teacher = teacher
            return cls
    raise HTTPException(status_code=404, detail="Class not found")
