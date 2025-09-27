from pydantic import BaseModel
from typing import List
from .student import Student

class Class(BaseModel):
    id: int
    name: str
    students: List[Student] = []
