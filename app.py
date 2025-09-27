import streamlit as st
import requests
import sys
import os

API_URL = "http://localhost:8000"  # Địa chỉ backend FastAPI

# __file__ = frontend/app.py
# BASE_DIR = thư mục gốc classmanager
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)  # ưu tiên tìm module ở thư mục gốc

import streamlit as st
import pandas as pd
from backend.logic import manager, Student, Teacher, Course, db

st.title("Class Manager")

# -----------------------------
# Quản lý lớp học (Class)
# -----------------------------
st.subheader("Create Class")
class_name = st.text_input("Class Name", key="class_name_input")
teacher_id_class = st.number_input("Teacher ID (Class)", min_value=1, key="teacher_id_class_input")
if st.button("Create Class", key="btn_create_class"):
    # Lấy ID mới dựa trên số lượng hiện tại
    classes = requests.get(f"{API_URL}/classes/").json()
    new_id = len(classes) + 1
    response = requests.post(f"{API_URL}/classes/", json={
        "id": new_id,
        "name": class_name,
        "teacher_id": teacher_id_class
    })
    st.success(response.json()["message"])

# -----------------------------
# Quản lý giáo viên (Teacher)
# -----------------------------
st.subheader("Add Teacher")
teacher_name = st.text_input("Teacher Name", key="teacher_name_input")
subject_ids = st.text_input("Subject IDs (comma separated)", key="teacher_subject_ids_input")
teacher_id_teacher = st.number_input("Teacher ID (Teacher)", min_value=1, key="teacher_id_teacher_input")
if st.button("Add Teacher", key="btn_add_teacher"):
    subject_ids_list = [int(x.strip()) for x in subject_ids.split(",") if x.strip().isdigit()]
    response = requests.post(f"{API_URL}/teachers/", json={
        "id": teacher_id_teacher,
        "name": teacher_name,
        "subject_ids": subject_ids_list
    })
    st.success(response.json()["message"])

# -----------------------------
# Quản lý học sinh (Student)
# -----------------------------
st.subheader("Add Student")
student_name = st.text_input("Student Name", key="student_name_input")
class_id_student = st.number_input("Class ID (Student)", min_value=1, key="class_id_student_input")
student_id_student = st.number_input("Student ID", min_value=1, key="student_id_student_input")
if st.button("Add Student", key="btn_add_student"):
    response = requests.post(f"{API_URL}/students/", json={
        "id": student_id_student,
        "name": student_name,
        "class_id": class_id_student
    })
    st.success(response.json()["message"])

# -----------------------------
# Quản lý môn học (Subject)
# -----------------------------
st.subheader("Add Subject")
subject_name = st.text_input("Subject Name", key="subject_name_input")
teacher_id_subject = st.number_input("Teacher ID (Subject)", min_value=1, key="teacher_id_subject_input")
subject_id_subject = st.number_input("Subject ID", min_value=1, key="subject_id_subject_input")
if st.button("Add Subject", key="btn_add_subject"):
    response = requests.post(f"{API_URL}/subjects/", json={
        "id": subject_id_subject,
        "name": subject_name,
        "teacher_id": teacher_id_subject
    })
    st.success(response.json()["message"])

# -----------------------------
# Quản lý thời khóa biểu (Schedule)
# -----------------------------
st.subheader("Add Schedule")
class_id_schedule = st.number_input("Class ID (Schedule)", min_value=1, key="class_id_schedule_input")
subject_id_schedule = st.number_input("Subject ID (Schedule)", min_value=1, key="subject_id_schedule_input")
day = st.text_input("Day", key="schedule_day_input")
time = st.text_input("Time", key="schedule_time_input")
schedule_id = st.number_input("Schedule ID", min_value=1, key="schedule_id_input")
if st.button("Add Schedule", key="btn_add_schedule"):
    response = requests.post(f"{API_URL}/schedules/", json={
        "id": schedule_id,
        "class_id": class_id_schedule,
        "subject_id": subject_id_schedule,
        "day": day,
        "time": time
    })
    st.success(response.json()["message"])

# -----------------------------
# Hiển thị dữ liệu
# -----------------------------
st.subheader("View Data")

if st.button("Refresh Classes", key="btn_refresh_classes"):
    response = requests.get(f"{API_URL}/classes/")
    st.write(response.json())

if st.button("Refresh Teachers", key="btn_refresh_teachers"):
    response = requests.get(f"{API_URL}/teachers/")
    st.write(response.json())

if st.button("Refresh Students", key="btn_refresh_students"):
    response = requests.get(f"{API_URL}/students/")
    st.write(response.json())

if st.button("Refresh Subjects", key="btn_refresh_subjects"):
    response = requests.get(f"{API_URL}/subjects/")
    st.write(response.json())

if st.button("Refresh Schedules", key="btn_refresh_schedules"):
    response = requests.get(f"{API_URL}/schedules/")
    st.write(response.json())
