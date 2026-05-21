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


-- Create the Fee Vouchers table
CREATE TABLE fee_vouchers (
    voucher_id INT IDENTITY(1000, 1) PRIMARY KEY, -- Starts at 1000 for realistic invoice numbers
    student_id INT NOT NULL,
    total_credits INT NOT NULL,
    tuition_fee DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Unpaid',
    issue_date DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT fk_voucher_student FOREIGN KEY (student_id) 
        REFERENCES students(id) 
        ON DELETE CASCADE
);
GO

-- 5. Insert some dummy data so you can test it immediately
-- 5. Insert some dummy data so you can test it immediately
INSERT INTO students (name, roll_no, department, semester) VALUES
('Aria', 'SE-045', 'Software Engineering', 3),
('Zane', 'CS-105', 'Computer Science', 1),
('Esha', 'AI-012', 'Artificial Intelligence', 5),
('Ryan', 'DS-088', 'Data Science', 4),
('Zara', 'SE-011', 'Software Engineering', 2),
('Kabir', 'CS-202', 'Computer Science', 6),
('Anaya', 'CY-033', 'Cyber Security', 3),
('Liam', 'SE-099', 'Software Engineering', 7),
('Mira', 'CS-110', 'Computer Science', 1),
('Dev', 'AI-054', 'Artificial Intelligence', 4),
('Sana', 'DS-023', 'Data Science', 2),
('Omar', 'SE-076', 'Software Engineering', 5),
('Tara', 'CS-301', 'Computer Science', 8),
('Arjun', 'CY-015', 'Cyber Security', 2),
('Riya', 'AI-089', 'Artificial Intelligence', 3);
GO

INSERT INTO courses (course_name, credit_hours) VALUES
('Introduction to Programming', 4),
('Object Oriented Programming', 4),
('Operating Systems', 3),
('Computer Networks', 3),
('Analysis of Algorithms', 3),
('Artificial Intelligence', 3),
('Machine Learning', 4),
('Information Security', 3),
('Web Engineering', 3),
('Discrete Structures', 3),
('Software Architecture and Design', 3),
('Compiler Construction', 3),
('Human Computer Interaction', 3),
('Digital Logic Design', 4),
('Cloud Computing', 3);
GO