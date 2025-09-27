from pydantic import BaseModel
from typing import List, Optional

class Class(BaseModel):
    id: int
    name: str
    teacher_id: int

class Teacher(BaseModel):
    id: int
    name: str
    subject_ids: List[int]

class Student(BaseModel):
    id: int
    name: str
    class_id: int

class Subject(BaseModel):
    id: int
    name: str
    teacher_id: int

class Schedule(BaseModel):
    id: int
    class_id: int
    subject_id: int
    day: str
    time: str
