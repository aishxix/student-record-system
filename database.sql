-- Create the database
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INT NOT NULL
);

-- Insert dummy data
INSERT INTO students (name, roll_no, department, semester) VALUES
('Aish', 'SE-042', 'Software Engineering', 3),
('John Doe', 'CS-101', 'Computer Science', 1),
('Jane Smith', 'EE-205', 'Electrical Engineering', 5),
('Ali Khan', 'SE-088', 'Software Engineering', 3);