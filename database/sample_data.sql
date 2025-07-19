-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS student_mgmt;
USE student_mgmt;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Person table (was personal_info)
CREATE TABLE IF NOT EXISTS person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    gender ENUM('Male', 'Female', 'Other'),
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Users table (references person)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    person_id INT,
    active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES person(id)
);

-- Create user_roles table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Addresses table
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    address_type ENUM('Home', 'Work', 'School', 'Other') DEFAULT 'Home',
    address_line1 VARCHAR(100) NOT NULL,
    address_line2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES person(id)
);

-- Contact info table
CREATE TABLE IF NOT EXISTS contact_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    contact_type ENUM('Phone', 'Email', 'Other') NOT NULL,
    contact_value VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES person(id)
);

-- Academic Session table
CREATE TABLE IF NOT EXISTS academic_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    credits INT DEFAULT 3,
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Course offerings in sessions
CREATE TABLE IF NOT EXISTS course_offerings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    course_id INT NOT NULL,
    faculty_id INT NOT NULL,
    max_students INT DEFAULT 50,
    current_students INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES academic_sessions(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (faculty_id) REFERENCES users(id)
);

-- Student course registrations
CREATE TABLE IF NOT EXISTS student_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    offering_id INT NOT NULL,
    registration_date DATE,
    status ENUM('Registered', 'Dropped', 'Completed') DEFAULT 'Registered',
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (offering_id) REFERENCES course_offerings(id),
    UNIQUE KEY unique_student_offering (student_id, offering_id)
);

-- Marks/Grades table
CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_id INT NOT NULL,
    assignment_type ENUM('Midterm', 'Final', 'Assignment', 'Project', 'Participation') NOT NULL,
    marks_obtained DECIMAL(5,2) NOT NULL,
    total_marks DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    percentage DECIMAL(5,2) GENERATED ALWAYS AS ((marks_obtained / total_marks) * 100) STORED,
    grade VARCHAR(2) GENERATED ALWAYS AS (
        CASE 
            WHEN percentage >= 90 THEN 'A+'
            WHEN percentage >= 80 THEN 'A'
            WHEN percentage >= 70 THEN 'B+'
            WHEN percentage >= 60 THEN 'B'
            WHEN percentage >= 50 THEN 'C+'
            WHEN percentage >= 40 THEN 'C'
            WHEN percentage >= 35 THEN 'D'
            ELSE 'F'
        END
    ) STORED,
    remarks TEXT,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (registration_id) REFERENCES student_registrations(id)
);

-- Degrees table
CREATE TABLE IF NOT EXISTS degrees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    abbreviation VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Student degree enrollments
CREATE TABLE IF NOT EXISTS student_degrees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    degree_id INT NOT NULL,
    enrollment_date DATE,
    expected_completion_date DATE,
    actual_completion_date DATE,
    status ENUM('Enrolled', 'In Progress', 'Completed', 'Dropped') DEFAULT 'Enrolled',
    create_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (degree_id) REFERENCES degrees(id)
);

-- Add roles
INSERT INTO roles (id, name) VALUES
(1, 'Administrator'),
(2, 'Faculty'),
(3, 'Student');

-- Add person records
INSERT INTO person (id, first_name, last_name, birth_date, gender) VALUES
(1, 'Admin', 'User', '1975-12-01', 'Other'),
(2, 'Priya', 'Ranjan', '2000-01-15', 'Male'),
(3, 'Anita', 'Sharma', '1980-05-20', 'Female'),
(4, 'Rahul', 'Verma', '2001-03-10', 'Male'),
(5, 'Sunita', 'Devi', '1999-07-25', 'Female'),
(6, 'Rajesh', 'Kumar', '1978-08-15', 'Male'),
(7, 'Meera', 'Patel', '2002-11-20', 'Female'),
(8, 'Amit', 'Singh', '2000-06-12', 'Male');

-- Add users (linked to person)
INSERT INTO users (id, username, password, person_id, active) VALUES
(1, 'admin', 'password123', 1, TRUE),
(2, 'student1', 'password123', 2, TRUE),
(3, 'faculty1', 'password123', 3, TRUE),
(4, 'student2', 'password123', 4, TRUE),
(5, 'student3', 'password123', 5, TRUE),
(6, 'faculty2', 'password123', 6, TRUE),
(7, 'student4', 'password123', 7, TRUE),
(8, 'student5', 'password123', 8, TRUE);

-- Add user_roles
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), -- admin is Administrator
(2, 3), -- student1 is Student
(3, 2), -- faculty1 is Faculty
(4, 3), -- student2 is Student
(5, 3), -- student3 is Student
(6, 2), -- faculty2 is Faculty
(7, 3), -- student4 is Student
(8, 3); -- student5 is Student

-- Add addresses
INSERT INTO addresses (person_id, address_type, address_line1, address_line2, city, state, postal_code, country, is_active) VALUES
(1, 'Work', '789 Admin Ave', NULL, 'Mumbai', 'Maharashtra', '400001', 'India', TRUE),
(2, 'Home', '123 Main St', NULL, 'Patna', 'Bihar', '800001', 'India', TRUE),
(3, 'Home', '456 College Rd', NULL, 'Delhi', 'Delhi', '110001', 'India', TRUE),
(4, 'Home', '12 Park Lane', NULL, 'Kolkata', 'West Bengal', '700001', 'India', TRUE),
(5, 'Home', '34 Lake View', NULL, 'Chennai', 'Tamil Nadu', '600001', 'India', TRUE),
(6, 'Home', '78 Faculty St', NULL, 'Bangalore', 'Karnataka', '560001', 'India', TRUE),
(7, 'Home', '90 Student Ave', NULL, 'Hyderabad', 'Telangana', '500001', 'India', TRUE),
(8, 'Home', '45 Campus Rd', NULL, 'Pune', 'Maharashtra', '411001', 'India', TRUE);

-- Add contact_info
INSERT INTO contact_info (person_id, contact_type, contact_value, is_active) VALUES
(1, 'Email', 'admin@example.com', TRUE),
(1, 'Phone', '+91-9000000003', FALSE),
(2, 'Phone', '+91-9000000001', TRUE),
(2, 'Email', 'priya.ranjan@example.com', TRUE),
(3, 'Phone', '+91-9000000002', TRUE),
(3, 'Email', 'anita.sharma@example.com', TRUE),
(4, 'Phone', '+91-9000000004', TRUE),
(5, 'Email', 'sunita.devi@example.com', TRUE),
(6, 'Phone', '+91-9000000005', TRUE),
(6, 'Email', 'rajesh.kumar@example.com', TRUE),
(7, 'Phone', '+91-9000000006', TRUE),
(7, 'Email', 'meera.patel@example.com', TRUE),
(8, 'Phone', '+91-9000000007', TRUE),
(8, 'Email', 'amit.singh@example.com', TRUE);

-- Add academic sessions
INSERT INTO academic_sessions (name, start_date, end_date, is_active) VALUES
('Fall 2024', '2024-08-01', '2024-12-15', TRUE),
('Spring 2025', '2025-01-15', '2025-05-30', TRUE),
('Summer 2025', '2025-06-01', '2025-07-31', FALSE);

-- Add degrees
INSERT INTO degrees (name, abbreviation, description) VALUES
('Bachelor of Technology in Computer Science', 'B.Tech CS', '4-year undergraduate program in Computer Science'),
('Bachelor of Technology in Information Technology', 'B.Tech IT', '4-year undergraduate program in Information Technology'),
('Master of Technology in Computer Science', 'M.Tech CS', '2-year postgraduate program in Computer Science'),
('Bachelor of Science in Mathematics', 'B.Sc Math', '3-year undergraduate program in Mathematics');

-- Add courses
INSERT INTO courses (code, name, description, credits) VALUES
('CS101', 'Introduction to Computer Science', 'Basic concepts of computer science and programming', 3),
('CS201', 'Data Structures and Algorithms', 'Advanced data structures and algorithm analysis', 4),
('CS301', 'Database Management Systems', 'Database design, SQL, and database administration', 4),
('CS401', 'Software Engineering', 'Software development lifecycle and methodologies', 3),
('IT101', 'Information Technology Fundamentals', 'Basic IT concepts and applications', 3),
('MATH101', 'Calculus I', 'Differential and integral calculus', 4),
('MATH201', 'Linear Algebra', 'Vector spaces, matrices, and linear transformations', 3),
('CS501', 'Advanced Programming', 'Advanced programming concepts and techniques', 4);

-- Add course offerings
INSERT INTO course_offerings (session_id, course_id, faculty_id, max_students, current_students) VALUES
(1, 1, 3, 50, 0), -- CS101 in Fall 2024 by faculty1
(1, 2, 3, 40, 0), -- CS201 in Fall 2024 by faculty1
(1, 3, 6, 35, 0), -- CS301 in Fall 2024 by faculty2
(1, 4, 6, 30, 0), -- CS401 in Fall 2024 by faculty2
(1, 5, 3, 45, 0), -- IT101 in Fall 2024 by faculty1
(1, 6, 6, 40, 0), -- MATH101 in Fall 2024 by faculty2
(2, 1, 3, 50, 0), -- CS101 in Spring 2025 by faculty1
(2, 2, 6, 40, 0), -- CS201 in Spring 2025 by faculty2
(2, 7, 3, 35, 0), -- MATH201 in Spring 2025 by faculty1
(2, 8, 6, 30, 0); -- CS501 in Spring 2025 by faculty2

-- Add student degree enrollments
INSERT INTO student_degrees (student_id, degree_id, enrollment_date, expected_completion_date, status) VALUES
(2, 1, '2022-08-01', '2026-05-30', 'In Progress'),
(4, 1, '2022-08-01', '2026-05-30', 'In Progress'),
(5, 2, '2022-08-01', '2026-05-30', 'In Progress'),
(7, 1, '2023-08-01', '2027-05-30', 'In Progress'),
(8, 2, '2023-08-01', '2027-05-30', 'In Progress');
