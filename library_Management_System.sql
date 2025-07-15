CREATE DATABASE library;
USE library;

-- Creating the Books table
CREATE TABLE Books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Available'
);

-- Creating the Students table
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50),
    class VARCHAR(10)
);

-- Creating the Issue table to track book issuance
CREATE TABLE Issue (
    issue_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    student_id INT,
    issue_date DATE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Inserting sample data into Books table
INSERT INTO Books (book_id, title, author, status) VALUES
(1, 'To Kill a Mockingbird', 'Harper Lee', 'Available'),
(2, '1984', 'George Orwell', 'Available'),
(3, 'Pride and Prejudice', 'Jane Austen', 'Available'),
(4, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Available'),
(5, 'Moby Dick', 'Herman Melville', 'Available');

select * from Books;

-- Inserting sample data into Students table
INSERT INTO Students (student_id, name, class) VALUES
(101, 'John Smith', '10A'),
(102, 'Emma Johnson', '11B'),
(103, 'Michael Brown', '12C'),
(104, 'Sarah Davis', '10B'),
(105, 'David Wilson', '11A');

select * from Students;

SELECT status FROM Books WHERE book_id = "%s"