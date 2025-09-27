import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Class Manager")

# Quản lý lớp học
st.subheader("Create Class")
class_name = st.text_input("Class Name")
teacher_id = st.number_input("Teacher ID", min_value=1)
if st.button("Create Class"):
    response = requests.post(f"{API_URL}/classes/", json={"id": len(classes)+1, "name": class_name, "teacher_id": teacher_id})
    st.success(response.json()["message"])

# Quản lý giáo viên
st.subheader("Add Teacher")
teacher_name = st.text_input("Teacher Name")
subject_ids = st.text_input("Subject IDs (comma separated)")
if st.button("Add Teacher"):
    subject_ids = list(map(int, subject_ids.split(",")))
    response = requests.post(f"{API_URL}/teachers/", json={"id": len(teachers)+1, "name": teacher_name, "subject_ids": subject_ids})
    st.success(response.json()["message"])

# Quản lý học sinh
st.subheader("Add Student")
student_name = st.text_input("Student Name")
class_id = st.number_input("Class ID", min_value=1)
if st.button("Add Student"):
    response = requests.post(f"{API_URL}/students/", json={"id": len(students)+1, "name": student_name, "class_id": class_id})
    st.success(response.json()["message"])

# Quản lý môn học
st.subheader("Add Subject")
subject_name = st.text_input("Subject Name")
teacher_id = st.number_input("Teacher ID", min_value=1)
if st.button("Add Subject"):
    response = requests.post(f"{API_URL}/subjects/", json={"id": len(subjects)+1, "name": subject_name, "teacher_id": teacher_id})
    st.success(response.json()["message"])

# Quản lý thời khóa biểu
st.subheader("Add Schedule")
class_id = st.number_input("Class ID", min_value=1)
subject_id = st.number_input("Subject ID", min_value=1)
day = st.text_input("Day")
time = st.text_input("Time")
if st.button("Add Schedule"):
    response = requests.post(f"{API_URL}/schedules/", json={"id": len(schedules)+1, "class_id": class_id, "subject_id": subject_id, "day": day, "time": time})
    st.success(response.json()["message"])

# Hiển thị dữ liệu
st.subheader("Classes")
if st.button("Refresh Classes"):
    response = requests.get(f"{API_URL}/classes/")
    st.write(response.json())

st.subheader("Teachers")
if st.button("Refresh Teachers"):
    response = requests.get(f"{API_URL}/teachers/")
    st.write(response.json())

st.subheader("Students")
if st.button("Refresh Students"):
    response = requests.get(f"{API_URL}/students/")
    st.write(response.json())

st.subheader("Subjects")
if st.button("Refresh Subjects"):
    response = requests.get(f"{API_URL}/subjects/")
    st.write(response.json())

st.subheader("Schedules")
if st.button("Refresh Schedules"):
    response = requests.get(f"{API_URL}/schedules/")
    st.write(response.json())
