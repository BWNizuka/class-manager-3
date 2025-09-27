from fastapi import FastAPI
from backend.controllers import student_controller, class_controller

app = FastAPI()

app.include_router(student_controller.router, prefix="/students", tags=["Students"])
app.include_router(class_controller.router, prefix="/classes", tags=["Classes"])
