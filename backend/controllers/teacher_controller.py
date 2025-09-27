from fastapi import APIRouter, HTTPException
from backend.models.teacher import Teacher

router = APIRouter()

teachers_db = []

@router.get("/")
def get_teachers():
    return teachers_db

@router.post("/")
def create_teacher(teacher: Teacher):
    teachers_db.append(teacher)
    return teacher

@router.get("/{teacher_id}")
def get_teacher(teacher_id: int):
    for teacher in teachers_db:
        if teacher.id == teacher_id:
            return teacher
    raise HTTPException(status_code=404, detail="Teacher not found")
