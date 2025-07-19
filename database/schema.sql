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