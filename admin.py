import mysql.connector
import streamlit as st
import pandas as pd
from ad_exam_list import option_edit_delete
from ad_result import result_edit_delete
from ad_exam_center import center_edit_delete
import matplotlib.pyplot as plt
from io import BytesIO

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="Exam_center_db"
    )
def is_admin_id_valid(admin_id):
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT adminID FROM users WHERE adminID = %s", (admin_id,))
        return bool(c.fetchone())
    
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

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(df["ExamID"], df["NumRegistrations"], color='Lavender')
        plt.xlabel('Exam ID')
        plt.ylabel('Number of Registrations')
        plt.title('Top 5 Exams with Most Registrations')
        plt.xticks(rotation=45)

        # Save the plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Display the plot in Streamlit
        st.image(image_stream.getvalue(), use_column_width=True)

def display_result_table():
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT * FROM Result")
        result_data = c.fetchall()
        df = pd.DataFrame(result_data, columns=["RegisterID", "Name", "ExamDuration", "TotalMarks"])
        st.dataframe(df)


def display_registered_students():
    with get_database_connection() as mydb:
        c = mydb.cursor()
    # Fetch the list of registered students from the database
        c.execute("SELECT * FROM Registration")
        registration_data = c.fetchall()

        if registration_data:
            df = pd.DataFrame(registration_data, columns=["RegisterID", "RegistrationDate", "StudentID", "ExamID","ExamName"])
            st.dataframe(df)
        else:
            st.warning("No registered students found.")



def admin_view_page():
    if "page" not in st.session_state:
        st.session_state.page=0

    login_placeholder= st.empty()

    if st.session_state.page==0:
        with login_placeholder.container():
            st.subheader("Login")

            username = st.text_input("Admin ID")
            password = st.text_input("Password:", type="password")
            login_button = st.button("Login")

            if login_button:
                if is_admin_id_valid(username):
                    st.success("Login successful!")
                    st.session_state.page= 1
                else:
                    st.error("Login failed. Check your username and password.")


    if st.session_state.page== 1:
        with login_placeholder.container():
            st.subheader("Admin Portal")
            st.info("**Welcome to the admin portal!!**")
            col1, col2= st.columns(2)
            with col1:
                st.subheader("Registered Students")
                display_registered_students()
            with col2:
                most_registered_exams_chart()
            view_op= st.selectbox("Select a View",["","Exam List","Exam Center List","Results"]) 
            

            if view_op=="Exam List":
                option_edit_delete()
            elif view_op=="Exam Center List":
                st.subheader("Exam Center")
                center_edit_delete()
            elif view_op=="Results":
                st.subheader("Results")
                result_edit_delete()

    


    