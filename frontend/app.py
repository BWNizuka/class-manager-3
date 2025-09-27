import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Class Manager")

menu = ["Students", "Classes"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Students":
    st.subheader("Students")
    
    # List students
    if st.button("Refresh Students"):
        response = requests.get(f"{API_URL}/students/")
        if response.status_code == 200:
            students = response.json()
            st.write(students)
        else:
            st.error("Failed to fetch students")
    
    # Add student
    with st.form("Add Student"):
        st.write("Add new student")
        student_id = st.number_input("ID", min_value=1)
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        submitted = st.form_submit_button("Add Student")
        if submitted:
            student = {"id": student_id, "name": name, "age": age}
            response = requests.post(f"{API_URL}/students/", json=student)
            if response.status_code == 200:
                st.success("Student added!")
            else:
                st.error("Failed to add student")

elif choice == "Classes":
    st.subheader("Classes")
    
    # List classes
    if st.button("Refresh Classes"):
        response = requests.get(f"{API_URL}/classes/")
        if response.status_code == 200:
            classes = response.json()
            st.write(classes)
        else:
            st.error("Failed to fetch classes")
    
    # Add class
    with st.form("Add Class"):
        st.write("Add new class")
        class_id = st.number_input("ID", min_value=1, key="class_id")
        class_name = st.text_input("Name", key="class_name")
        submitted = st.form_submit_button("Add Class")
        if submitted:
            cls = {"id": class_id, "name": class_name, "students": []}
            response = requests.post(f"{API_URL}/classes/", json=cls)
            if response.status_code == 200:
                st.success("Class added!")
            else:
                st.error("Failed to add class")
                
elif choice == "Teachers":
    st.subheader("Teachers")
    
    # List teachers
    if st.button("Refresh Teachers"):
        response = requests.get(f"{API_URL}/teachers/")
        if response.status_code == 200:
            teachers = response.json()
            st.write(teachers)
        else:
            st.error("Failed to fetch teachers")
    
    # Add teacher
    with st.form("Add Teacher"):
        st.write("Add new teacher")
        teacher_id = st.number_input("ID", min_value=1, key="teacher_id")
        name = st.text_input("Name", key="teacher_name")
        subject = st.text_input("Subject", key="teacher_subject")
        submitted = st.form_submit_button("Add Teacher")
        if submitted:
            teacher = {"id": teacher_id, "name": name, "subject": subject}
            response = requests.post(f"{API_URL}/teachers/", json=teacher)
            if response.status_code == 200:
                st.success("Teacher added!")
            else:
                st.error("Failed to add teacher")
