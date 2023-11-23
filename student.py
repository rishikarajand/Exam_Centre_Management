import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from std_result_page import results_page
from std_reg_page import registration_page

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )
def student_details_display(studentID):
    with get_database_connection() as mydb:
            st.subheader("Student Details")
            c = mydb.cursor()
            c.execute("SELECT StudentID, Name, Email, DateOfBirth, Age, AddressS FROM Student WHERE StudentID = %s", (studentID,))
            student_dets = c.fetchone()
            # df = pd.DataFrame(student_dets, columns=["StudentID", "Name", "Email", "DateOfBirth", "Age", "AddressS"])
            # st.dataframe(df)
            if student_dets:
                student_id, name, email, dob, age, address = student_dets
                col1, col2, col3 = st.columns(3)
                # Display each piece of information individually
                with col1:
                    st.info(f"Student ID: {student_id}")
                    st.info(f"Date of Birth: {dob}")
                
                with col2:
                    st.info(f"Name: {name}")
                    st.info(f"Address: {address}")

                with col3:
                    st.info(f"Age: {age}")
                    st.info(f"Email: {email}")
            else:
                st.warning("No student details found for the entered Student ID.")

def most_registered_exams_chart():
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("""
            SELECT ExamID, COUNT(*) as num_registrations
            FROM Registration
            GROUP BY ExamID
            ORDER BY num_registrations DESC
            LIMIT 5
        """)
        data = c.fetchall()
        df = pd.DataFrame(data, columns=["ExamID", "NumRegistrations"])
        custom_colors=["#d4afb9", "#d1cfe2","#9cadce", "#7ec4cf", "#52b2cf"]
        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(df["NumRegistrations"], labels=df["ExamID"], autopct='%1.1f%%', startangle=140, colors=custom_colors)
        plt.title('Top 5 Exams with Most Registrations')

        # Save the plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Display the plot in Streamlit
        st.image(image_stream.getvalue(), use_column_width=True)


def display_exam_table():
    with get_database_connection() as mydb:
        c = mydb.cursor()
         # Call the stored procedure
        c.callproc("display_exam_table")

        # Fetch the results
        for result in c.stored_results():
            exam_data = result.fetchall()


        # Display the results using Streamlit
        st.subheader("Exam Table")
        df = pd.DataFrame(exam_data, columns=["ExamID", "ExamName", "ExamDate", "ExamDuration", "TotalMarks"])
        st.dataframe(df)

def is_student_id_valid(student_id):
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT StudentID FROM Student WHERE StudentID = %s", (student_id,))
        return bool(c.fetchone())

def student_view_page():
    global studentID    # Initialize studentID outside of the conditional blocks and stores student id after session expires 

    if "page" not in st.session_state:
        st.session_state.page = 0

    login_placeholder = st.empty() 

    if st.session_state.page == 0: 
        with login_placeholder.container():
            st.subheader("Student Portal")
            studentID = st.text_input("Student ID")
            login_button_placeholder = st.empty()

            if login_button_placeholder.button("Login"):
                if is_student_id_valid(studentID):
                    st.success("Login successful!")
                    st.session_state.page = 1
                    login_button_placeholder.empty()
                else:
                    st.error("Invalid Student ID. Please try again.")
    # studID= studentID
    if st.session_state.page == 1:
        with login_placeholder.container():
            student_details_display(studentID)

            col1, col2 = st.columns(2)
            # Column 1: Display Student Details
            with col1:
                display_exam_table()
            # Column 2: Display Most Registered Exams Chart and Exam Table
            with col2:
                most_registered_exams_chart()

            st.subheader("Result Or Registeration")
            option = st.selectbox("Select Option", ["", "Result", "Register"])
            if option == "Result":
                results_page(studentID)
            elif option == "Register":
                registration_page(studentID)
