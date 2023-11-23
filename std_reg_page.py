import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import re
from room_seat_alloc import allocate_seats
def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )

def get_existing_registration_ids():
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT RegisterID FROM Registration")
        return [row[0] for row in c.fetchall()]

def generate_unique_registration_id():
    existing_ids = get_existing_registration_ids()

    while True:
        registration_id = f"Reg{uuid.uuid4().hex[:3].upper()}"
        if registration_id not in existing_ids:
            return registration_id


def registration_page(check_stdID):
        st.subheader("Exam Registration")

        # Form to register for an exam
        student_id = st.text_input("Enter Student ID")
        exam_name = st.text_input("Enter Exam Name")
        exam_ID = st.text_input("Enter Exam ID")
        registration_date = datetime.now().strftime("%Y-%m-%d")
        registration_id = generate_unique_registration_id() #Correct the reg id part


        
        if st.button("Submit"):
        # Fetch student name
            with get_database_connection() as mydb:
                if student_id==check_stdID:
                    c = mydb.cursor()
                    c.execute("SELECT Name FROM Student WHERE StudentID = %s", (student_id,))
                    result = c.fetchone()
                    student_name = result[0]
                # st.write(f"Student Name: {student_name}")
                # else:
                #     st.error("Inncorect studentID entered ")
                

        # Fetch date of the exam
                    exam_date_query = "SELECT ExamDate FROM Exam WHERE ExamID = %s"
                    with get_database_connection() as mydb:
                        c = mydb.cursor()
                        c.execute(exam_date_query, (exam_ID,))
                        exam_date_res = c.fetchone()
                        exam_date= exam_date_res[0]

                # Fetch center name and location
                    center_info_query = "SELECT CenterName, Location FROM ExamCenter WHERE ExamID = %s"
                    with get_database_connection() as mydb:
                        c = mydb.cursor()
                        c.execute(center_info_query, (exam_ID,))
                        center_info = c.fetchone() 

                    center_name, center_location = center_info
                    # Insert registration information into the database
                    with get_database_connection() as mydb:
                        c = mydb.cursor()
                        sql = "INSERT INTO Registration (RegisterID, RegistrationDate, StudentID, ExamID) VALUES (%s, %s, %s, %s)"
                        val = (registration_id, registration_date, student_id, exam_ID)
                        c.execute(sql, val)
                        mydb.commit()

                    # Display registration information
                    st.success("Registration Successful!")
                    st.subheader("Registration Details")

                    col1, col2= st.columns(2)

                    with col1 :
                        st.info(f"**Registration ID:**  {registration_id}")
                        st.info(f"**Student ID:**  {student_id}")
                        st.info(f"**Exam ID:**  {exam_ID}")
                        st.info(f"**Center Name:**  {center_name}")
                    with col2:
                        st.info(f"**Registration Date:**  {registration_date}")
                        st.info(f"**Student Name:**  {student_name}")
                        st.info(f"**Exam Date:**  {exam_date}")
                        st.info(f"**Center Location:**  {center_location}")
                    
                    # allocate_seats()
    
                else:
                    st.error("Inncorect studentID entered")
            


            

# registration_page()