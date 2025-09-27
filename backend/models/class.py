from pydantic import BaseModel
from typing import List, Optional
from .student import Student
from .teacher import Teacher

class Class(BaseModel):
    id: int
    name: str
    students: List[Student] = []
    teacher: Optional[Teacher] = None
