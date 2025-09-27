class ClassManager:
    def __init__(self, students_col, teachers_col, courses_col):
        self.students_col = students_col
        self.teachers_col = teachers_col
        self.courses_col = courses_col

    # -----------------------------
    # Student CRUD
    # -----------------------------
    def create_student(self, student: Student):
        if self.students_col.find_one({"student_id": student.person_id}):
            return False, "Student ID already exists"
        self.students_col.insert_one(student.to_dict())
        return True, "Student created"

    def read_students(self):
        return list(self.students_col.find({}, {"_id": 0}))

    def update_student(self, student_id, new_data: dict):
        result = self.students_col.update_one(
            {"student_id": student_id}, {"$set": new_data}
        )
        if result.matched_count == 0:
            return False, "Student not found"
        return True, "Student updated"

    def delete_student(self, student_id):
        result = self.students_col.delete_one({"student_id": student_id})
        if result.deleted_count == 0:
            return False, "Student not found"
        return True, "Student deleted"

    # -----------------------------
    # Teacher CRUD
    # -----------------------------
    def create_teacher(self, teacher: Teacher):
        if self.teachers_col.find_one({"teacher_id": teacher.person_id}):
            return False, "Teacher ID already exists"
        self.teachers_col.insert_one(teacher.to_dict())
        return True, "Teacher created"

    def read_teachers(self):
        return list(self.teachers_col.find({}, {"_id": 0}))

    def update_teacher(self, teacher_id, new_data: dict):
        result = self.teachers_col.update_one(
            {"teacher_id": teacher_id}, {"$set": new_data}
        )
        if result.matched_count == 0:
            return False, "Teacher not found"
        return True, "Teacher updated"

    def delete_teacher(self, teacher_id):
        result = self.teachers_col.delete_one({"teacher_id": teacher_id})
        if result.deleted_count == 0:
            return False, "Teacher not found"
        return True, "Teacher deleted"

    # -----------------------------
    # Course CRUD
    # -----------------------------
    def create_course(self, course: Course):
        if self.courses_col.find_one({"course_code": course.code}):
            return False, "Course code already exists"
        self.courses_col.insert_one(course.to_dict())
        return True, "Course created"

    def read_courses(self):
        return list(self.courses_col.find({}, {"_id": 0}))

    def update_course(self, course_code, new_data: dict):
        result = self.courses_col.update_one(
            {"course_code": course_code}, {"$set": new_data}
        )
        if result.matched_count == 0:
            return False, "Course not found"
        return True, "Course updated"

    def delete_course(self, course_code):
        result = self.courses_col.delete_one({"course_code": course_code})
        if result.deleted_count == 0:
            return False, "Course not found"
        return True, "Course deleted"

    # -----------------------------
    # Assignments
    # -----------------------------
    def assign_teacher(self, teacher_id, course_code):
        t = self.teachers_col.find_one({"teacher_id": teacher_id})
        c = self.courses_col.find_one({"course_code": course_code})
        if not t or not c:
            return False, "Teacher or course not found"
        self.courses_col.update_one({"course_code": course_code}, {"$set": {"teacher_id": teacher_id}})
        if course_code not in t.get("courses", []):
            self.teachers_col.update_one({"teacher_id": teacher_id}, {"$push": {"courses": course_code}})
        return True, "Teacher assigned"

    def enroll_student(self, student_id, course_code):
        s = self.students_col.find_one({"student_id": student_id})
        c = self.courses_col.find_one({"course_code": course_code})
        if not s or not c:
            return False, "Student or course not found"
        if student_id not in c.get("students", []):
            self.courses_col.update_one({"course_code": course_code}, {"$push": {"students": student_id}})
        if course_code not in s.get("enrollments", []):
            self.students_col.update_one({"student_id": student_id}, {"$push": {"enrollments": course_code}})
        return True, "Student enrolled"
