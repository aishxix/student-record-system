USE student_db;
GO

-- 1. Drop existing tables carefully to avoid foreign key conflicts
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
GO

-- 2. Core Student Record Entity
CREATE TABLE students (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INT NOT NULL
);
GO

-- 3. Catalog Dimension Entity 
CREATE TABLE courses (
    course_id INT IDENTITY(1,1) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit_hours INT NOT NULL
);
GO

-- 4. Many-to-Many Junction Table (Connects Students and Courses)
CREATE TABLE enrollments (
    enrollment_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    
    -- Relational Integrity Mapping Constraints
    CONSTRAINT fk_student FOREIGN KEY (student_id) 
        REFERENCES students(id) 
        ON DELETE CASCADE,
        
    CONSTRAINT fk_course FOREIGN KEY (course_id) 
        REFERENCES courses(course_id) 
        ON DELETE CASCADE
);
GO

-- 5. Insert some dummy data so you can test it immediately
INSERT INTO students (name, roll_no, department, semester) VALUES
('Aish', 'SE-042', 'Software Engineering', 3),
('John Doe', 'CS-101', 'Computer Science', 1);

INSERT INTO courses (course_name, credit_hours) VALUES
('Database Management Systems', 3),
('Data Structures', 4),
('Software Requirement Engineering', 3);
GO