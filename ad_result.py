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

def display_results():
    st.subheader("Results Table")
    with get_database_connection() as mydb:
        c = mydb.cursor()
        c.execute("SELECT * FROM Result")
        result_data = c.fetchall()

        if result_data:
            df = pd.DataFrame(result_data, columns=["RegisterID","Marks Obtained","Grade","Exam Name"])
            st.dataframe(df)
        else:
            st.info("No data found in the Results table.")

def add_result():
    if "page" not in st.session_state:
        st.session_state.page = 0

    result_placeholder = st.empty()

    if st.session_state.page == 0:
        with result_placeholder.container():
            # display_results()

            add_button = st.button("Add Result")
            if add_button:
                st.session_state.page = 1

    if st.session_state.page == 1:
        with result_placeholder.container():
            st.subheader("Add Result")
            regID = st.text_input("Register ID")
            total_marks = st.number_input("Marks")
            exam_name = st.text_input("Exam Name")

            # Use st.radio for grade input
            grade_options = ["Pass", "Fail"]
            grade = st.radio("Select Grade", grade_options)

            if st.button("Save Result"):
                with get_database_connection() as mydb:
                    c = mydb.cursor()
                    # Ensure 'MarksObtained' is an integer column
                    sql = "INSERT INTO Result (RegisterID, MarksObtained, Grade, ExamName) VALUES (%s, %s, %s, %s)"
                    val = (regID, total_marks, grade, exam_name)
                    c.execute(sql, val)
                    mydb.commit()
                st.success("Result added successfully")
                st.session_state.page = 0
                display_results()
def update_result():
    if "page" not in st.session_state:
        st.session_state.page = 0

    entry_placeholder = st.empty()

    if st.session_state.page == 0:
        with entry_placeholder.container():
            st.subheader("Update Result Entry")
            register_id_to_update = st.text_input("Enter Register ID to update")


            if st.button("Enter"):
                st.session_state.page=1
                update_placeholder= st.empty()
                with get_database_connection() as mydb:
                    c = mydb.cursor()
                    # Check if the register ID exists before updating
                    c.execute("SELECT * FROM Result WHERE RegisterID = %s", (register_id_to_update,))
                    result = c.fetchall()
                if st.session_state.page==1:
                    with update_placeholder.container():
                            if result:
                                existing_entry= result[0]
                                st.write(f"**Existing Result Entry for Register ID {register_id_to_update}:**")
                                # Display the existing entry for reference
                                col1, col2= st.columns(2)
                                with col1:
                                    st.info(f"Register ID: {register_id_to_update}")
                                    st.info(f"Marks: {existing_entry[1]}")
                                with col2:
                                    st.info(f"Grade: {existing_entry[2]}")
                                    st.info(f"Exam Name: {existing_entry[3]}")
                                # Get updated information from the user
                                updated_marks = st.number_input("Enter updated Marks", value=existing_entry[1])
                                updated_grade = st.selectbox("Select updated Grade", ["pass","fail"])
                                updated_exam_name = st.text_input("Enter updated Exam Name", value=existing_entry[3])
                                if st.button("Update Result"):
                                    # Perform the update
                                    c.execute("UPDATE Result SET MarksObtained = %s, Grade = %s, ExamName = %s WHERE RegisterID = %s",
                                            (updated_marks, updated_grade, updated_exam_name, register_id_to_update))
                                    mydb.commit()
                                    st.success(f"Result with Register ID {register_id_to_update} updated successfully.")
                                    display_results()
                                else:
                                    st.warning(f"No Result found with Register ID {register_id_to_update}.")
# def update_result():
#     if "update_result_state" not in st.session_state:
#         st.session_state.update_result_state = {
#             "page": 0,
#             "register_id_to_update": "",
#             "existing_entry": None,
#         }
#     st.subheader("Update Result Entry")
#     register_id_to_update = st.text_input("Enter Register ID to update")
#     # Check if the button was clicked
#     if st.button("Enter"):
#         # Get the register ID from the text input
#         # register_id_to_update = st.text_input(
#         #     "Enter Register ID to update",
#         #     value=st.session_state.update_result_state["register_id_to_update"],
#         # )

#         with get_database_connection() as mydb:
#             c = mydb.cursor()

#             # Check if the register ID exists before updating
#             c.execute("SELECT * FROM Result WHERE RegisterID = %s", (register_id_to_update,))
#             result = c.fetchall()

#             if result:
#                 existing_entry = result[0]
#                 st.session_state.update_result_state["register_id_to_update"] = register_id_to_update
#                 st.session_state.update_result_state["existing_entry"] = existing_entry

#                 st.write(
#                     f"**Existing Result Entry for Register ID {register_id_to_update}:**"
#                 )
#                 # Display the existing entry for reference
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.info(f"Register ID: {register_id_to_update}")
#                     st.info(f"Marks: {existing_entry[1]}")
#                 with col2:
#                     st.info(f"Grade: {existing_entry[2]}")
#                     st.info(f"Exam Name: {existing_entry[3]}")

#                 # Get updated information from the user
#                 st.session_state.update_result_state["page"] = 1
#                 updated_marks = st.number_input(
#                     "Enter updated Marks", value=existing_entry[1]
#                 )
#                 updated_grade = st.selectbox(
#                     "Select updated Grade", ["pass", "fail"], index=0 if existing_entry[2] == "pass" else 1
#                 )
#                 updated_exam_name = st.text_input(
#                     "Enter updated Exam Name", value=existing_entry[3]
#                 )

#                 if st.button("Update Result"):
#                     # Perform the update
#                     c.execute(
#                         "UPDATE Result SET MarksObtained = %s, Grade = %s, ExamName = %s WHERE RegisterID = %s",
#                         (
#                             updated_marks,
#                             updated_grade,
#                             updated_exam_name,
#                             register_id_to_update,
#                         ),
#                     )
#                     mydb.commit()
#                     st.success(
#                         f"Result with Register ID {register_id_to_update} updated successfully."
#                     )
#                     st.session_state.update_result_state["page"] = 0
#                     display_results()
#             else:
#                 st.warning(f"No Result found with Register ID {register_id_to_update}.")


def delete_result():
    st.subheader("Delete Result Entry")
    register_id_to_delete = st.text_input("Enter Register ID to delete")

    if st.button("Delete"):
        with get_database_connection() as mydb:
            c = mydb.cursor()
            # Check if the register ID exists before deleting
            c.execute("SELECT * FROM Result WHERE RegisterID = %s", (register_id_to_delete,))
            existing_entry = c.fetchone()

            if existing_entry:
                # Perform the deletion
                c.execute("DELETE FROM Result WHERE RegisterID = %s", (register_id_to_delete,))
                mydb.commit()
                st.success(f"Result with Register ID {register_id_to_delete} deleted successfully.")
                display_results()
            else:
                st.warning(f"No Result found with Register ID {register_id_to_delete}.")

def result_edit_delete():
        option= st.selectbox("Select Option",["View Table","Add","Delete"])
        if option=="View Table":
            display_results()
        if option=="Add":
            add_result()
        if option=="Delete":
            delete_result()
        # if option=="Update":
        #     update_result()
