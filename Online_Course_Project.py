import streamlit as st
import sqlite3

# Function to initialize the database and tables


def init_db():
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()

    # Create tables (courses, students)
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            course_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to add or update a course


def add_or_update_course(name, description, course_id=None):
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()

    if course_id:
        c.execute("UPDATE courses SET name = ?, description = ? WHERE id = ?",
                  (name, description, course_id))
    else:
        c.execute(
            "INSERT INTO courses (name, description) VALUES (?, ?)", (name, description))

    conn.commit()
    conn.close()

# Function to view all courses and the number of students joined each course


def view_courses():
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()
    c.execute("SELECT courses.name, courses.description, courses.id FROM courses")
    courses = c.fetchall()
    conn.close()
    return courses

# Function to delete a course


def delete_course(course_id):
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()

# Function to add or update a student


def add_or_update_student(name, email, phone, course_id, student_id=None):
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()

    if student_id:
        c.execute("UPDATE students SET name = ?, email = ?, phone = ?, course_id = ? WHERE id = ?",
                  (name, email, phone, course_id, student_id))
    else:
        c.execute("INSERT INTO students (name, email, phone, course_id) VALUES (?, ?, ?, ?)",
                  (name, email, phone, course_id))

    conn.commit()
    conn.close()

# Function to view all students


def view_students():
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return students

# Function to delete a student


def delete_student(student_id):
    conn = sqlite3.connect('course_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


# Streamlit app
st.title("Online Course Management System")

# Initialize the database
init_db()

# Sidebar for selecting user type (Student or Teacher) - On the left side
user_type = st.sidebar.radio("Login as", ("Teacher", "Student"))

# Display CRUD options based on the selected user type - On the right side
if user_type == "Student":
  #  st.write( "Student operations: Update profile, View courses, Join a course, Leave a course")

    # Allow students to update their profile
    st.header("Student Profile")
    student_name = st.text_input("Your Name")
    student_email = st.text_input("Your Email")
    student_phone = st.text_input("Your Phone")
    student_course_id = st.text_input("Your Course ID")
    if st.button("Save"):
        # Update student details
        # Assuming students don't have a specific course yet
        add_or_update_student(student_name, student_email,
                              student_phone, student_course_id)
        st.success("Profile Saved Successfully!")

    # Display existing courses
    st.header("Available Courses")
    courses = view_courses()
    if courses:
        st.write("Courses:")
        course_data = [(course[0], course[1], course[2]) for course in courses]
        st.table(course_data)

        # Allow students to join a course
        st.write("Join a Course:")
        selected_course_id = st.text_input("Enter Course ID to join")
        if st.button("Join Course"):
            add_or_update_student(None, None, None, selected_course_id)
            st.success("You have successfully joined the course!")
    else:
        st.write("No courses available.")

    # Allow students to leave a course
    st.header("Leave a Course")
    st.write("Leave a Course:")
    course_id_to_leave = st.text_input("Enter Course ID to leave")
    if st.button("Leave Course"):
        # Update student's course to None
        add_or_update_student(None, None, None, None, course_id_to_leave)
        st.success("You have left the course.")

elif user_type == "Teacher":
    #st.write("Teacher operations: Add/Update/View/Delete courses")

    # Teacher sidebar options
    teacher_options = ["Manage Courses", "Manage Students"]
    selected_option = st.sidebar.radio("Select an option", teacher_options)

    if selected_option == "Manage Courses":
     #   st.write("Course operations: Add/Update/View/Delete courses")

        # Sidebar for adding, updating, viewing, or deleting a course
        st.sidebar.header("Course Actions")
        action = st.sidebar.selectbox("Select an action", [
                                      "Add Course", "Update Course", "View Courses", "Delete Course"])
        if action == "Add Course":
            course_name = st.sidebar.text_input("Course Name")
            course_description = st.sidebar.text_area("Course Description")
            if st.sidebar.button(action):
                add_or_update_course(course_name, course_description)
                st.sidebar.success("Course added successfully!")

        elif action == "Update Course":
            course_id = st.sidebar.selectbox("Select Course ID to update", [
                                             course[2] for course in view_courses()])
            course_name = st.sidebar.text_input("New Course Name")
            course_description = st.sidebar.text_area("New Course Description")
            if st.sidebar.button(action):
                add_or_update_course(
                    course_name, course_description, course_id)
                st.sidebar.success("Course updated successfully!")

        elif action == "View Courses":
            # Display existing courses
            st.header("Available Courses")
            courses = view_courses()
            if courses:
                st.write("Courses:")
                course_data = [(course[0], course[1], course[2])
                               for course in courses]
                st.table(course_data)
            else:
                st.write("No courses available.")

        elif action == "Delete Course":
            course_id = st.sidebar.selectbox("Select Course ID to delete", [
                                             course[2] for course in view_courses()])
            if st.sidebar.button(action):
                delete_course(course_id)
                st.sidebar.success("Course deleted successfully!")

    elif selected_option == "Manage Students":
      #  st.write("Student operations: Add/Update/View/Delete students")

        # Sidebar for adding, updating, viewing, or deleting a student
        st.sidebar.header("Teacher Actions")
        student_name = st.sidebar.text_input("Student Name")
        student_email = st.sidebar.text_input("Student Email")
        student_phone = st.sidebar.text_input("Student Phone")
        student_course_id = st.sidebar.text_input("Course ID")
        action = st.sidebar.selectbox("Select an action", [
                                      "Add Student", "Update Student", "View Students", "Delete Student"])
        if action == "Add Student":
            if st.sidebar.button(action):
                add_or_update_student(
                    student_name, student_email, student_phone, student_course_id)
                st.sidebar.success("Student added successfully!")

        elif action == "Update Student":
            student_id = st.sidebar.selectbox("Select Student ID to update", [
                                              student[0] for student in view_students()])
            if st.sidebar.button(action):
                add_or_update_student(
                    student_name, student_email, student_phone, student_course_id, student_id)
                st.sidebar.success("Student updated successfully!")

        elif action == "View Students":
            # Display existing students
            st.header("Available Students")
            students = view_students()
            if students:
                student_data = [
                    (student[1], student[2], student[3], student[4]) for student in students]
                st.write("Students:")
                st.table(student_data)
            else:
                st.write("No students available.")

        elif action == "Delete Student":
            student_id = st.sidebar.selectbox("Select Student ID to delete", [
                                              student[0] for student in view_students()])
            if st.sidebar.button(action):
                delete_student(student_id)
                st.sidebar.success("Student deleted successfully!")
