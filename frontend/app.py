import sys
import os
import streamlit as st
import pandas as pd
from backend.logic import manager, Student, Teacher, Course, db

# -----------------------------
# Setup
# -----------------------------
# __file__ = frontend/app.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

st.set_page_config(page_title="Class Manager", layout="wide")
st.title("Class Manager")

if db is None:
    st.warning("❌ Không kết nối được tới MongoDB. Kiểm tra file .env và chuỗi MONGO_URI.")
    st.stop()

# Debug hiển thị trong sidebar
st.sidebar.caption(f"🔌 Using DB: {db.name}")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard", "Students", "Teachers", "Courses", "Assign Teacher", "Enroll Student"
])

# -----------------------------
# Dashboard
# -----------------------------
if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    st.metric("Students", len(manager.read_students()))
    st.metric("Teachers", len(manager.read_teachers()))
    st.metric("Courses", len(manager.read_courses()))

# -----------------------------
# Students CRUD
# -----------------------------
elif menu == "Students":
    st.subheader("Students CRUD")

    # Create
    with st.form("create_student"):
        st.write("➕ Add Student")
        sid = st.text_input("ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        grade = st.number_input("Grade level", 1, 20, 10)
        if st.form_submit_button("Add"):
            ok, msg = manager.create_student(Student(sid, name, email, int(grade)))
            st.success(msg) if ok else st.error(msg)

    # Update
    with st.form("update_student"):
        st.write("✏️ Update Student")
        sid = st.text_input("Student ID to update")
        new_name = st.text_input("New Name")
        new_email = st.text_input("New Email")
        new_grade = st.number_input("New Grade level", 1, 20, 10, key="update_grade")
        if st.form_submit_button("Update"):
            update_data = {}
            if new_name: update_data["name"] = new_name
            if new_email: update_data["email"] = new_email
            if new_grade: update_data["grade_level"] = int(new_grade)
            ok, msg = manager.update_student(sid, update_data)
            st.success(msg) if ok else st.error(msg)

    # Delete
    with st.form("delete_student"):
        st.write("🗑 Delete Student")
        sid = st.text_input("Student ID to delete", key="delete_student")
        if st.form_submit_button("Delete"):
            ok, msg = manager.delete_student(sid)
            st.success(msg) if ok else st.error(msg)

    st.dataframe(pd.DataFrame(manager.read_students()))

# -----------------------------
# Teachers CRUD
# -----------------------------
elif menu == "Teachers":
    st.subheader("Teachers CRUD")

    # Create
    with st.form("create_teacher"):
        st.write("➕ Add Teacher")
        tid = st.text_input("ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        spec = st.text_input("Specialization")
        if st.form_submit_button("Add"):
            ok, msg = manager.create_teacher(Teacher(tid, name, email, spec))
            st.success(msg) if ok else st.error(msg)

    # Update
    with st.form("update_teacher"):
        st.write("✏️ Update Teacher")
        tid = st.text_input("Teacher ID to update")
        new_name = st.text_input("New Name")
        new_email = st.text_input("New Email")
        new_spec = st.text_input("New Specialization")
        if st.form_submit_button("Update"):
            update_data = {}
            if new_name: update_data["name"] = new_name
            if new_email: update_data["email"] = new_email
            if new_spec: update_data["specialization"] = new_spec
            ok, msg = manager.update_teacher(tid, update_data)
            st.success(msg) if ok else st.error(msg)

    # Delete
    with st.form("delete_teacher"):
        st.write("🗑 Delete Teacher")
        tid = st.text_input("Teacher ID to delete", key="delete_teacher")
        if st.form_submit_button("Delete"):
            ok, msg = manager.delete_teacher(tid)
            st.success(msg) if ok else st.error(msg)

    st.dataframe(pd.DataFrame(manager.read_teachers()))

# -----------------------------
# Courses CRUD
# -----------------------------
elif menu == "Courses":
    st.subheader("Courses CRUD")

    # Create
    with st.form("create_course"):
        st.write("➕ Add Course")
        code = st.text_input("Course Code")
        title = st.text_input("Title")
        schedule = st.text_input("Schedule")
        if st.form_submit_button("Add"):
            ok, msg = manager.create_course(Course(code, title, schedule))
            st.success(msg) if ok else st.error(msg)

    # Update
    with st.form("update_course"):
        st.write("✏️ Update Course")
        code = st.text_input("Course Code to update")
        new_title = st.text_input("New Title")
        new_schedule = st.text_input("New Schedule")
        if st.form_submit_button("Update"):
            update_data = {}
            if new_title: update_data["title"] = new_title
            if new_schedule: update_data["schedule"] = new_schedule
            ok, msg = manager.update_course(code, update_data)
            st.success(msg) if ok else st.error(msg)

    # Delete
    with st.form("delete_course"):
        st.write("🗑 Delete Course")
        code = st.text_input("Course Code to delete", key="delete_course")
        if st.form_submit_button("Delete"):
            ok, msg = manager.delete_course(code)
            st.success(msg) if ok else st.error(msg)

    st.dataframe(pd.DataFrame(manager.read_courses()))

# -----------------------------
# Assign Teacher
# -----------------------------
elif menu == "Assign Teacher":
    st.subheader("Assign Teacher to Course")
    teachers = manager.read_teachers()
    courses = manager.read_courses()
    if teachers and courses:
        tid = st.selectbox("Teacher", [t["teacher_id"] for t in teachers])
        cid = st.selectbox("Course", [c["course_code"] for c in courses])
        if st.button("Assign"):
            ok, msg = manager.assign_teacher(tid, cid)
            st.success(msg) if ok else st.error(msg)
    else:
        st.info("Cần có teacher và course trước.")

# -----------------------------
# Enroll Student
# -----------------------------
elif menu == "Enroll Student":
    st.subheader("Enroll Student in Course")
    students = manager.read_students()
    courses = manager.read_courses()
    if students and courses:
        sid = st.selectbox("Student", [s["student_id"] for s in students])
        cid = st.selectbox("Course", [c["course_code"] for c in courses])
        if st.button("Enroll"):
            ok, msg = manager.enroll_student(sid, cid)
            st.success(msg) if ok else st.error(msg)
    else:
        st.info("Cần có student và course trước.")
