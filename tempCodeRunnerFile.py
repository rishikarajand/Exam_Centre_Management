import mysql.connector
import streamlit as st
from student import student_view_page
from admin import admin_view_page


def switch_page(page_function):
    page_function()
def main():
    st.title("Exam Center Management System")
    page = st.sidebar.selectbox("Select Page", ["Student View", "Admin View"])

    if page == "Student View":
        switch_page(student_view_page)
    elif page == "Admin View":
        switch_page(admin_view_page)

if __name__ == "__main__":
    main()
