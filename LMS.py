import mysql.connector
from datetime import date
import sys

# Database connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="312Jai97",
        database="library_setup"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    sys.exit(1)


# Function to issue a book
def issue_book():
    print("\nBOOK ISSUE")
    book_id = int(input("Enter Book ID: "))
    student_id = int(input("Enter Student ID: "))

    # MySQL Query: Check if the book exists and is available in the Books table
    # Purpose: Ensures the book is valid and not already issued
    cursor.execute("SELECT status FROM Books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if not result:
        print("Book not found!")
        return
    if result[0] != 'Available':
        print("Book is already issued!")
        return

    # MySQL Query: Verify if the student exists in the Students table
    # Purpose: Ensures the student ID is valid before issuing the book
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    if not cursor.fetchone():
        print("Student not found!")
        return

    # MySQL Query: Update the book's status to 'Issued' in the Books table
    # Purpose: Marks the book as unavailable for other users
    cursor.execute("UPDATE Books SET status = 'Issued' WHERE book_id = %s", (book_id,))

    # MySQL Query: Insert a record into the Issue table to track the issuance
    # Purpose: Logs the book issuance with the student ID and date
    cursor.execute("INSERT INTO Issue (book_id, student_id, issue_date) VALUES (%s, %s, %s)",
                   (book_id, student_id, date.today()))
    conn.commit()
    print("Book issued successfully!")


# Function to deposit a book
def deposit_book():
    print("\nBOOK DEPOSIT")
    book_id = int(input("Enter Book ID: "))

    # MySQL Query: Check if the book is issued in the Books table
    # Purpose: Ensures the book exists and is currently issued
    cursor.execute("SELECT status FROM Books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if not result:
        print("Book not found!")
        return
    if result[0] != 'Issued':
        print("Book is not issued!")
        return

    # MySQL Query: Update the book's status to 'Available' in the Books table
    # Purpose: Marks the book as available for other users
    cursor.execute("UPDATE Books SET status = 'Available' WHERE book_id = %s", (book_id,))

    # MySQL Query: Delete the issuance record from the Issue table
    # Purpose: Removes the record of the book being issued to a student
    cursor.execute("DELETE FROM Issue WHERE book_id = %s", (book_id,))
    conn.commit()
    print("Book deposited successfully!")


# Function to create a student record
def create_student():
    print("\nCREATE STUDENT RECORD")
    student_id = int(input("Enter Student ID: "))
    name = input("Enter Student Name: ")
    class_name = input("Enter Class: ")

    try:
        # MySQL Query: Insert a new student record into the Students table
        # Purpose: Adds a new student to the database
        cursor.execute("INSERT INTO Students (student_id, name, class) VALUES (%s, %s, %s)",
                       (student_id, name, class_name))
        conn.commit()
        print("Student record created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to display all students
def display_all_students():
    print("\nALL STUDENTS RECORD")
    # MySQL Query: Retrieve all records from the Students table
    # Purpose: Fetches and displays all student details
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    if not students:
        print("No students found!")
        return
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Class: {student[2]}")


# Function to display a specific student
def display_specific_student():
    print("\nDISPLAY SPECIFIC STUDENT RECORD")
    student_id = int(input("Enter Student ID: "))
    # MySQL Query: Retrieve a specific student record from the Students table
    # Purpose: Fetches details of a student with the given ID
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if student:
        print(f"ID: {student[0]}, Name: {student[1]}, Class: {student[2]}")
    else:
        print("Student not found!")


# Function to modify a student record
def modify_student():
    print("\nMODIFY STUDENT RECORD")
    student_id = int(input("Enter Student ID: "))
    # MySQL Query: Check if the student exists in the Students table
    # Purpose: Verifies the student ID before attempting to modify
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    if not cursor.fetchone():
        print("Student not found!")
        return
    name = input("Enter New Name: ")
    class_name = input("Enter New Class: ")
    # MySQL Query: Update the student record in the Students table
    # Purpose: Modifies the student's name and class
    cursor.execute("UPDATE Students SET name = %s, class = %s WHERE student_id = %s",
                   (name, class_name, student_id))
    conn.commit()
    print("Student record modified successfully!")


# Function to delete a student record
def delete_student():
    print("\nDELETE STUDENT RECORD")
    student_id = int(input("Enter Student ID: "))
    # MySQL Query: Check if the student exists in the Students table
    # Purpose: Verifies the student ID before attempting to delete
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    if not cursor.fetchone():
        print("Student not found!")
        return
    # MySQL Query: Delete the student record from the Students table
    # Purpose: Removes the student from the database
    cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
    conn.commit()
    print("Student record deleted successfully!")


# Function to create a book record
def create_book():
    print("\nCREATE BOOK RECORD")
    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    try:
        # MySQL Query: Insert a new book record into the Books table
        # Purpose: Adds a new book to the database with 'Available' status
        cursor.execute("INSERT INTO Books (book_id, title, author, status) VALUES (%s, %s, %s, 'Available')",
                       (book_id, title, author))
        conn.commit()
        print("Book record created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to display all books
def display_all_books():
    print("\nALL BOOKS RECORD")
    # MySQL Query: Retrieve all records from the Books table
    # Purpose: Fetches and displays all book details
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    if not books:
        print("No books found!")
        return
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {book[3]}")


# Function to display a specific book
def display_specific_book():
    print("\nDISPLAY SPECIFIC BOOK RECORD")
    book_id = int(input("Enter Book ID: "))
    # MySQL Query: Retrieve a specific book record from the Books table
    # Purpose: Fetches details of a book with the given ID
    cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if book:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {book[3]}")
    else:
        print("Book not found!")


# Function to modify a book record
def modify_book():
    print("\nMODIFY BOOK RECORD")
    book_id = int(input("Enter Book ID: "))
    # MySQL Query: Check if the book exists in the Books table
    # Purpose: Verifies the book ID before attempting to modify
    cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
    if not cursor.fetchone():
        print("Book not found!")
        return
    title = input("Enter New Title: ")
    author = input("Enter New Author: ")
    # MySQL Query: Update the book record in the Books table
    # Purpose: Modifies the book's title and author
    cursor.execute("UPDATE Books SET title = %s, author = %s WHERE book_id = %s",
                   (title, author, book_id))
    conn.commit()
    print("Book record modified successfully!")


# Function to delete a book record
def delete_book():
    print("\nDELETE BOOK RECORD")
    book_id = int(input("Enter Book ID: "))
    # MySQL Query: Check if the book exists in the Books table
    # Purpose: Verifies the book ID before attempting to delete
    cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
    if not cursor.fetchone():
        print("Book not found!")
        return
    # MySQL Query: Delete the book record from the Books table
    # Purpose: Removes the book from the database
    cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
    conn.commit()
    print("Book record deleted successfully!")


# Administration menu
def admin_menu():
    while True:
        print("\nADMINISTRATION MENU")
        print("1. CREATE STUDENT RECORD")
        print("2. DISPLAY ALL STUDENTS RECORD")
        print("3. DISPLAY SPECIFIC STUDENT RECORD")
        print("4. MODIFY STUDENT RECORD")
        print("5. DELETE STUDENT RECORD")
        print("6. CREATE BOOK")
        print("7. DISPLAY ALL BOOKS")
        print("8. DISPLAY SPECIFIC BOOK")
        print("9. MODIFY BOOK")
        print("10. DELETE BOOK RECORD")
        print("11. BACK TO MAIN MENU")
        choice = input("Enter choice (1-11): ")

        if choice == '1':
            create_student()
        elif choice == '2':
            display_all_students()
        elif choice == '3':
            display_specific_student()
        elif choice == '4':
            modify_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            create_book()
        elif choice == '7':
            display_all_books()
        elif choice == '8':
            display_specific_book()
        elif choice == '9':
            modify_book()
        elif choice == '10':
            delete_book()
        elif choice == '11':
            break
        else:
            print("Invalid choice! Please try again.")


# Main menu
def main():
    while True:
        print("\nLIBRARY MANAGEMENT SYSTEM")
        print("1. BOOK ISSUE")
        print("2. BOOK DEPOSIT")
        print("3. ADMINISTRATION MENU")
        print("4. EXIT")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            issue_book()
        elif choice == '2':
            deposit_book()
        elif choice == '3':
            admin_menu()
        elif choice == '4':
            print("Exiting system. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()