from fastapi import FastAPI
from models import Class, Teacher, Student, Subject, Schedule

app = FastAPI()

# Danh sách giả lập
classes = []
teachers = []
students = []
subjects = []
schedules = []

@app.post("/classes/")
def create_class(class_: Class):
    classes.append(class_)
    return {"message": f"Class {class_.name} created successfully."}

@app.post("/teachers/")
def create_teacher(teacher: Teacher):
    teachers.append(teacher)
    return {"message": f"Teacher {teacher.name} added successfully."}

@app.post("/students/")
def create_student(student: Student):
    students.append(student)
    return {"message": f"Student {student.name} added successfully."}

@app.post("/subjects/")
def create_subject(subject: Subject):
    subjects.append(subject)
    return {"message": f"Subject {subject.name} added successfully."}

@app.post("/schedules/")
def create_schedule(schedule: Schedule):
    schedules.append(schedule)
    return {"message": f"Schedule for {schedule.class_id} added successfully."}

@app.get("/classes/")
def get_classes():
    return classes

@app.get("/teachers/")
def get_teachers():
    return teachers

@app.get("/students/")
def get_students():
    return students

@app.get("/subjects/")
def get_subjects():
    return subjects

@app.get("/schedules/")
def get_schedules():
    return schedules
