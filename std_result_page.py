import mysql.connector
import streamlit as st
import pandas as pd

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )

def results_page(check_stdID):
    st.subheader("View Result")
    student_id = st.text_input("Enter Student ID")

    with get_database_connection() as mydb:
        c = mydb.cursor()

        if st.button("View Result"):
            if student_id==check_stdID:
            # Fetch the result information from the database
                c.execute("SELECT * FROM Result WHERE RegisterID IN (SELECT RegisterID FROM Registration WHERE StudentID = %s)", (student_id,))
                result_data = c.fetchall()

                if result_data:
                    result = result_data[0]  # Assuming only one result is fetched

                    col1, col2= st.columns(2)
                    with col1:
                        st.info(f"***Register ID:*** {result[0]}")
                        st.info(f"***Exam:*** {result[3]}")
                    with col2:
                        st.info(f"***Marks Obtained:*** {result[1]}")
                        st.warning(f"***Grade:*** {result[2]}")
                        

            else:
                st.error("Incorrect Student ID.")

# results_page()
