import streamlit as st
import mysql.connector
import pandas as pd
from student import display_exam_table


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )

        
def edit_exam_list():
    if "page" not in st.session_state:
        st.session_state.page = 0

    exam_placeholder = st.empty()

    if st.session_state.page == 0:
        with exam_placeholder.container():
            # with get_database_connection() as mydb:
            #     c = mydb.cursor()
            #     c.execute("SELECT * FROM Exam")
            #     exam_data = c.fetchall()
            #     df = pd.DataFrame(exam_data, columns=["ExamID", "ExamName", "ExamDuration", "TotalMarks"])
            #     st.dataframe(df)

            edit_button = st.button("Edit")
            if edit_button:
                st.session_state.page = 1

    if st.session_state.page == 1:
        with exam_placeholder.container():
            st.subheader("Edit")
            examID = st.text_input("Exam ID")
            exam_name = st.text_input("Exam Name")
            exam_duration = st.number_input("Exam Duration")
            exam_date= st.date_input("Exam Date")
            total_marks = st.number_input("Marks")
            if st.button("Add"):
                with get_database_connection() as mydb:
                    c = mydb.cursor()
                    sql = "INSERT INTO Exam (ExamID, ExamName, ExamDate, ExamDuration, TotalMarks) VALUES (%s, %s, %s, %s, %s)"
                    val = (examID, exam_name, exam_date, exam_duration, total_marks)
                    c.execute(sql, val)
                    mydb.commit()
                st.success("Updated successfully")
                st.session_state.page = 0
                display_exam_table()

# Display the edited exam list
# edit_exam_list()

def delete_exam_entry():
    st.subheader("Delete Exam Entry")
    exam_id_to_delete = st.text_input("Enter Exam ID to delete")

    if st.button("Delete"):
        with get_database_connection() as mydb:
            c = mydb.cursor()
            # Check if the exam ID exists before deleting
            c.execute("SELECT * FROM Exam WHERE ExamID = %s", (exam_id_to_delete,))
            existing_entry = c.fetchone()

            if existing_entry:
                # Perform the deletion
                c.execute("DELETE FROM Exam WHERE ExamID = %s", (exam_id_to_delete,))
                mydb.commit()
                st.success(f"Exam entry with ID {exam_id_to_delete} deleted successfully.")
                display_exam_table()
            else:
                st.warning(f"No exam entry found with ID {exam_id_to_delete}.")

def option_edit_delete():
    option= st.selectbox("Select Option",["View Table","Add","Delete"])
    if option=="View Table":
        display_exam_table()
    if option=="Add":
        edit_exam_list()
    if option=="Delete":
        delete_exam_entry()





