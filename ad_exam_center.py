import streamlit as st
import mysql.connector
import pandas as pd


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )

def display_exam_center():
    st.subheader("Exam Centre Table")

    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT * FROM ExamCenter")
        exam_center_data = c.fetchall()

        if exam_center_data:
            df = pd.DataFrame(exam_center_data, columns=["CenterID", "CenterName", "Location", "RoomID", "ExamID","RegisterID"])
            st.dataframe(df)
        else:
            st.info("No data found in the Exam Center table.")
        
def add_exam_center():
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
                # display_exam_center()

                edit_button = st.button("Edit")
                if edit_button:
                    st.session_state.page = 1

    if st.session_state.page == 1:
        with exam_placeholder.container():
            st.subheader("Edit")
            centerID= st.text_input("Center ID")
            center_name = st.text_input("Center Name")
            indian_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
             "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
             "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
             "West Bengal", "Chandigarh", "Delhi", "Puducherry"]
            Location = st.selectbox("Select Location",indian_states)
            if st.button("Add"):
                with get_database_connection() as mydb:
                    c = mydb.cursor()
                    sql = "INSERT INTO ExamCenter (CenterID, CenterName, Location) VALUES (%s, %s, %s)"
                    val = (centerID, center_name, Location)
                    c.execute(sql, val)
                    mydb.commit()
                st.success("Updated successfully")
                st.session_state.page = 0
                display_exam_center()

# Display the edited exam list
# edit_exam_list()

def delete_exam_center():
    st.subheader("Delete Exam Entry")
    center_id_to_delete = st.text_input("Enter Centre ID to delete")

    if st.button("Delete"):
        with get_database_connection() as mydb:
            c = mydb.cursor()
            # Check if the exam ID exists before deleting
            c.execute("SELECT * FROM examcenter WHERE CenterID = %s", (center_id_to_delete,))
            existing_entry = c.fetchone()

            if existing_entry:
                c.execute("DELETE FROM examcenter WHERE CenterID = %s", (center_id_to_delete,))
                mydb.commit() 
                st.success(f"Centre with ID {center_id_to_delete} deleted successfully.")
                display_exam_center()
            else:
                st.warning(f"No Centre found with ID {center_id_to_delete}.")

def center_edit_delete():
    option= st.selectbox("Select Option",["View Table","Add","Delete"])
    if option=="View Table":
        display_exam_center()
    if option=="Add":
        add_exam_center()
    if option=="Delete":
        delete_exam_center()

