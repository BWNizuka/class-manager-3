from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    grade: str
    email: str
