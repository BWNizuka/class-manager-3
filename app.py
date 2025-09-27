import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Địa chỉ backend FastAPI

st.title("Class Manager")

# -----------------------------
# 1️⃣ Quản lý lớp học (Class)
# -----------------------------
st.subheader("Create Class")
class_name = st.text_input("Class Name", key="class_name")
teacher_id_class = st.number_input("Teacher ID (Class)", min_value=1, key="teacher_id_class")
if st.button("Create Class", key="btn_create_class"):
    response = requests.post(f"{API_URL}/classes/", json={
        "id": len(requests.get(f"{API_URL}/classes/").json()) + 1,
        "name": class_name,
        "teacher_id": teacher_id_class
    })
    st.success(response.json()["message"])

# -----------------------------
# 2️⃣ Quản lý giáo viên (Teacher)
# -----------------------------
st.subheader("Add Teacher")
teacher_name = st.text_input("Teacher Name", key="teacher_name")
subject_ids = st.text_input("Subject IDs (comma separated)", key="teacher_subject_ids")
teacher_id_teacher = st.number_input("Teacher ID (Teacher)", min_value=1, key="teacher_id_teacher")
if st.button("Add Teacher", key="btn_add_teacher"):
    subject_ids_list = [int(x.strip()) for x in subject_ids.split(",") if x.strip().isdigit()]
    response = requests.post(f"{API_URL}/teachers/", json={
        "id": teacher_id_teacher,
        "name": teacher_name,
        "subject_ids": subject_ids_list
    })
    st.success(response.json()["message"])

# -----------------------------
# 3️⃣ Quản lý học sinh (Student)
# -----------------------------
st.subheader("Add Student")
student_name = st.text_input("Student Name", key="student_name")
class_id_student = st.number_input("Class ID (Student)", min_value=1, key="class_id_student")
student_id_student = st.number_input("Student ID", min_value=1, key="student_id")
if st.button("Add Student", key="btn_add_student"):
    response = requests.post(f"{API_URL}/students/", json={
        "id": student_id_student,
        "name": student_name,
        "class_id": class_id_student
    })
    st.success(response.json()["message"])

# -----------------------------
# 4️⃣ Quản lý môn học (Subject)
# -----------------------------
st.subheader("Add Subject")
subject_name = st.text_input("Subject Name", key="subject_name")
teacher_id_subject = st.number_input("Teacher ID (Subject)", min_value=1, key="teacher_id_subject")
subject_id_subject = st.number_input("Subject ID", min_value=1, key="subject_id")
if st.button("Add Subject", key="btn_add_subject"):
    response = requests.post(f"{API_URL}/subjects/", json={
        "id": subject_id_subject,
        "name": subject_name,
        "teacher_id": teacher_id_subject
    })
    st.success(response.json()["message"])

# -----------------------------
# 5️⃣ Quản lý thời khóa biểu (Schedule)
# -----------------------------
st.subheader("Add Schedule")
class_id_schedule = st.number_input("Class ID (Schedule)", min_value=1, key="class_id_schedule")
subject_id_schedule = st.number_input("Subject ID (Schedule)", min_value=1, key="subject_id_schedule")
day = st.text_input("Day", key="schedule_day")
time = st.text_input("Time", key="schedule_time")
schedule_id = st.number_input("Schedule ID", min_value=1, key="schedule_id")
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
# 6️⃣ Hiển thị dữ liệu
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
