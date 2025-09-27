# backend/logic.py
from abc import ABC, abstractmethod
from pymongo import MongoClient
from dotenv import dotenv_values

# -----------------------------
# Load biến môi trường từ .env
# -----------------------------
config = dotenv_values(".env")
MONGO_URI = config.get("MONGO_URI")
DB_NAME = config.get("DB_NAME", "classmanager")

# -----------------------------
# Kết nối MongoDB
# -----------------------------
def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
        client.admin.command("ping")  # test kết nối
        return client[DB_NAME]
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

db = get_db()
if db is not None:
    students_col = db["students"]
    teachers_col = db["teachers"]
    courses_col = db["courses"]
else:
    students_col = teachers_col = courses_col = None

# -----------------------------
# OOP Classes
# -----------------------------
class Person(ABC):
    def __init__(self, person_id: str, name: str, email: str):
        self.person_id = person_id
        self.name = name
        self.email = email

    @abstractmethod
    def to_dict(self):
        pass

class Student(Person):
    def __init__(self, person_id, name, email, grade_level):
        super().__init__(person_id, name, email)
        self.grade_level = grade_level
        self.enrollments = []

    def to_dict(self):
        return {
            "student_id": self.person_id,
            "name": self.name,
            "email": self.email,
            "grade_level": self.grade_level,
            "enrollments": self.enrollments
        }

class Teacher(Person):
    def __init__(self, person_id, name, email, specialization):
        super().__init__(person_id, name, email)
        self.specialization = specialization
        self.courses = []

    def to_dict(self):
        return {
            "teacher_id": self.person_id,
            "name": self.name,
            "email": self.email,
            "specialization": self.specialization,
            "courses": self.courses
        }

class Course:
    def __init__(self, code, title, schedule):
        self.code = code
        self.title = title
        self.schedule = schedule
        self.teacher_id = None
        self.students = []

    def to_dict(self):
        return {
            "course_code": self.code,
            "title": self.title,
            "schedule": self.schedule,
            "teacher_id": self.teacher_id,
            "students": self.students
        }

# -----------------------------
# Controller (ClassManager)
# -----------------------------
class ClassManager:
    def __init__(self, students_col, teachers_col, courses_col):
        self.students_col = students_col
        self.teachers_col = teachers_col
        self.courses_col = courses_col

    # Student CRUD
    def create_student(self, student: Student):
        if self.students_col.find_one({"student_id": student.person_id}):
            return False, "Student ID already exists"
        self.students_col.insert_one(student.to_dict())
        return True, "Student created"

    def read_students(self):
        return list(self.students_col.find({}, {"_id": 0}))

    # Teacher CRUD
    def create_teacher(self, teacher: Teacher):
        if self.teachers_col.find_one({"teacher_id": teacher.person_id}):
            return False, "Teacher ID already exists"
        self.teachers_col.insert_one(teacher.to_dict())
        return True, "Teacher created"

    def read_teachers(self):
        return list(self.teachers_col.find({}, {"_id": 0}))

    # Course CRUD
    def create_course(self, course: Course):
        if self.courses_col.find_one({"course_code": course.code}):
            return False, "Course code already exists"
        self.courses_col.insert_one(course.to_dict())
        return True, "Course created"

    def read_courses(self):
        return list(self.courses_col.find({}, {"_id": 0}))

    # Assignments
    def assign_teacher(self, teacher_id, course_code):
        t = self.teachers_col.find_one({"teacher_id": teacher_id})
        c = self.courses_col.find_one({"course_code": course_code})
        if not t or not c:
            return False, "Teacher or course not found"
        self.courses_col.update_one({"course_code": course_code}, {"$set": {"teacher_id": teacher_id}})
        if course_code not in t.get("courses", []):
            self.teachers_col.update_one({"teacher_id": teacher_id}, {"$push": {"courses": course_code}})
        return True, "Teacher assigned"

    def enroll_student(self, student_id, course_code):
        s = self.students_col.find_one({"student_id": student_id})
        c = self.courses_col.find_one({"course_code": course_code})
        if not s or not c:
            return False, "Student or course not found"
        if student_id not in c.get("students", []):
            self.courses_col.update_one({"course_code": course_code}, {"$push": {"students": student_id}})
        if course_code not in s.get("enrollments", []):
            self.students_col.update_one({"student_id": student_id}, {"$push": {"enrollments": course_code}})
        return True, "Student enrolled"

manager = ClassManager(students_col, teachers_col, courses_col) if db is not None else None
