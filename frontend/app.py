import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Đảm bảo backend đang chạy tại URL này

st.set_page_config(page_title="Class Manager", layout="wide")
st.title("Class Manager System")

menu = ["Students", "Teachers", "Classes"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------- STUDENTS -------------------
if choice == "Students":
    st.subheader("Students")

    if st.button("Refresh Students"):
        try:
            res = requests.get(f"{API_URL}/students/")
            res.raise_for_status()
            students = res.json()
            st.table(students)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch students: {e}")

    with st.form("Add Student"):
        st.write("Add new student")
        student_id = st.number_input("ID", min_value=1)
        name = st.text_input("Name")
        grade = st.text_input("Grade")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            student = {"id": student_id, "name": name, "grade": grade, "email": email}
            try:
                res = requests.post(f"{API_URL}/students/", json=student)
                res.raise_for_status()
                st.success("Student added!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add student: {e}")

# ------------------- TEACHERS -------------------
elif choice == "Teachers":
    st.subheader("Teachers")

    if st.button("Refresh Teachers"):
        try:
            res = requests.get(f"{API_URL}/teachers/")
            res.raise_for_status()
            teachers = res.json()
            st.table(teachers)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch teachers: {e}")

    with st.form("Add Teacher"):
        st.write("Add new teacher")
        teacher_id = st.number_input("ID", min_value=1, key="teacher_id")
        name = st.text_input("Name", key="teacher_name")
        subject = st.text_input("Subject", key="teacher_subject")
        email = st.text_input("Email", key="teacher_email")
        submitted = st.form_submit_button("Add Teacher")
        if submitted:
            teacher = {"id": teacher_id, "name": name, "subject": subject, "email": email}
            try:
                res = requests.post(f"{API_URL}/teachers/", json=teacher)
                res.raise_for_status()
                st.success("Teacher added!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add teacher: {e}")

# ------------------- CLASSES -------------------
elif choice == "Classes":
    st.subheader("Classes")

    if st.button("Refresh Classes"):
        try:
            res = requests.get(f"{API_URL}/classes/")
            res.raise_for_status()
            classes = res.json()
            st.table(classes)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch classes: {e}")

    # ----------------- Add Class -----------------
    with st.form("Add Class"):
        st.write("Add new class")
        class_id = st.number_input("ID", min_value=1, key="class_id")
        class_name = st.text_input("Name", key="class_name")
        submitted = st.form_submit_button("Add Class")
        if submitted:
            cls = {"id": class_id, "name": class_name, "students": [], "teacher": None}
            try:
                res = requests.post(f"{API_URL}/classes/", json=cls)
                res.raise_for_status()
                st.success("Class added!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add class: {e}")

    st.markdown("---")
    st.subheader("Manage Class")
    
    class_id = st.number_input("Class ID", min_value=1, key="class_action_id")
    action = st.selectbox("Action", ["Add Student", "Assign Teacher"])

    # ----------------- Add Student to Class -----------------
    if action == "Add Student":
        student_id = st.number_input("Student ID", min_value=1, key="action_student_id")
        student_name = st.text_input("Student Name", key="action_student_name")
        student_grade = st.text_input("Student Grade", key="action_student_grade")
        student_email = st.text_input("Student Email", key="action_student_email")
        if st.button("Add Student to Class"):
            student = {
                "id": student_id,
                "name": student_name,
                "grade": student_grade,
                "email": student_email
            }
            try:
                res = requests.post(f"{API_URL}/classes/{class_id}/add_student", json=student)
                res.raise_for_status()
                st.success("Student added to class!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add student to class: {e}")

    # ----------------- Assign Teacher to Class -----------------
    elif action == "Assign Teacher":
        teacher_id = st.number_input("Teacher ID", min_value=1, key="action_teacher_id")
        teacher_name = st.text_input("Teacher Name", key="action_teacher_name")
        teacher_subject = st.text_input("Teacher Subject", key="action_teacher_subject")
        teacher_email = st.text_input("Teacher Email", key="action_teacher_email")
        if st.button("Assign Teacher to Class"):
            teacher = {
                "id": teacher_id,
                "name": teacher_name,
                "subject": teacher_subject,
                "email": teacher_email
            }
            try:
                res = requests.post(f"{API_URL}/classes/{class_id}/assign_teacher", json=teacher)
                res.raise_for_status()
                st.success("Teacher assigned to class!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to assign teacher: {e}")
