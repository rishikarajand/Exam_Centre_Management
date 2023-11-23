import streamlit as st
import mysql.connector
import random

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinku$2003",
        database="exam_center_db"
    )

def allocate_seats():
    with get_database_connection() as mydb:
        c = mydb.cursor()

        # Get the list of available rooms and their capacities
        c.execute("SELECT RoomID FROM ExamRoom")
        rooms = [row[0] for row in c.fetchall()]

        # Get the list of available seats
        c.execute("SELECT SeatID FROM Seat")
        all_seats = [row[0] for row in c.fetchall()]

        # Get the list of registered students
        c.execute("SELECT StudentID FROM Registration")
        students = [row[0] for row in c.fetchall()]

        # Shuffle the list of students to randomize seat assignments
        random.shuffle(students)

        # Display allocation information in Streamlit
        st.subheader("Seat Allocation Results")

        # Iterate through each student and assign a seat
        for student in students:
            # Check if there are available rooms
            if not rooms:
                st.warning("No Currently available rooms for seat allocation.")
                break

            # Choose a random room
            room = random.choice(rooms)

            # Check if there are available seats in the chosen room
            room_seats = [seat for seat in all_seats if seat.startswith(room)]
            if not room_seats:
                # st.warning(f"No available seats in Room {room}. Skipping.")
                rooms.remove(room)
                continue

            # Choose a random seat in the chosen room
            chosen_seat = random.choice(room_seats)

            # Remove the chosen seat from the list of available seats
            all_seats.remove(chosen_seat)

            # Assign the seat to the student
            c.execute("UPDATE Seat SET StudentID = %s WHERE SeatID = %s", (student, chosen_seat))
            mydb.commit()

            st.write(f"Assigned Seat {chosen_seat} to Student {student} in Room {room}")
