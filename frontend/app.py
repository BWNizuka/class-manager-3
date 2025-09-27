import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Class Manager", layout="wide")
st.title("Class Manager System")

# Khởi tạo session_state để lưu dữ liệu
if "students" not in st.session_state:
    st.session_state.students = []

if "teachers" not in st.session_state:
    st.session_state.teachers = []

if "classes" not in st.session_state:
    st.session_state.classes = []

menu = ["Students", "Teachers", "Classes"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------- STUDENTS -------------------
if choice == "Students":
    st.subheader("Students")

    if st.button("Refresh Students"):
        res = requests.get(f"{API_URL}/students/")
        if res.ok:
            st.session_state.students = res.json()
        else:
            st.error("Failed to fetch students")

    if st.session_state.students:
        st.table(st.session_state.students)

    with st.form("Add Student"):
        st.write("Add new student")
        student_id = st.number_input("ID", min_value=1)
        name = st.text_input("Name")
        grade = st.text_input("Grade")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            student = {"id": student_id, "name": name, "grade": grade, "email": email}
            res = requests.post(f"{API_URL}/students/", json=student)
            if res.ok:
                st.success("Student added!")
                st.session_state.students.append(student)
            else:
                st.error("Failed to add student")

# ------------------- TEACHERS -------------------
elif choice == "Teachers":
    st.subheader("Teachers")

    if st.button("Refresh Teachers"):
        res = requests.get(f"{API_URL}/teachers/")
        if res.ok:
            st.session_state.teachers = res.json()
        else:
            st.error("Failed to fetch teachers")

    if st.session_state.teachers:
        st.table(st.session_state.teachers)

    with st.form("Add Teacher"):
        st.write("Add new teacher")
        teacher_id = st.number_input("ID", min_value=1, key="teacher_id")
        name = st.text_input("Name", key="teacher_name")
        subject = st.text_input("Subject", key="teacher_subject")
        email = st.text_input("Email", key="teacher_email")
        submitted = st.form_submit_button("Add Teacher")
        if submitted:
            teacher = {"id": teacher_id, "name": name, "subject": subject, "email": email}
            res = requests.post(f"{API_URL}/teachers/", json=teacher)
            if res.ok:
                st.success("Teacher added!")
                st.session_state.teachers.append(teacher)
            else:
                st.error("Failed to add teacher")

# ------------------- CLASSES -------------------
elif choice == "Classes":
    st.subheader("Classes")

    if st.button("Refresh Classes"):
        res = requests.get(f"{API_URL}/classes/")
        if res.ok:
            st.session_state.classes = res.json()
        else:
            st.error("Failed to fetch classes")

    if st.session_state.classes:
        st.table(st.session_state.classes)

    # ----------------- Add Class -----------------
    with st.form("Add Class"):
        st.write("Add new class")
        class_id = st.number_input("ID", min_value=1, key="class_id")
        class_name = st.text_input("Name", key="class_name")
        submitted = st.form_submit_button("Add Class")
        if submitted:
            cls = {"id": class_id, "name": class_name, "students": [], "teacher": None}
            res = requests.post(f"{API_URL}/classes/", json=cls)
            if res.ok:
                st.success("Class added!")
                st.session_state.classes.append(cls)
            else:
                st.error("Failed to add class")

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
            res = requests.post(f"{API_URL}/classes/{class_id}/add_student", json=student)
            if res.ok:
                st.success("Student added to class!")
                # Cập nhật session_state.classes
                for cls in st.session_state.classes:
                    if cls["id"] == class_id:
                        cls["students"].append(student)
                        break
            else:
                st.error("Failed to add student to class")

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
            res = requests.post(f"{API_URL}/classes/{class_id}/assign_teacher", json=teacher)
            if res.ok:
                st.success("Teacher assigned to class!")
                # Cập nhật session_state.classes
                for cls in st.session_state.classes:
                    if cls["id"] == class_id:
                        cls["teacher"] = teacher
                        break
            else:
                st.error("Failed to assign teacher")
