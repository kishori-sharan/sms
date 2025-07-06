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
(5, 'Sunita', 'Devi', '1999-07-25', 'Female');

-- Add users (linked to person)
INSERT INTO users (id, username, password, person_id) VALUES
(1, 'admin', 'password123', 1),
(2, 'student', 'password123', 2),
(3, 'faculty', 'password123', 3);

-- Add user_roles
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), -- admin is Administrator
(2, 3), -- student is Student
(3, 2); -- faculty is Faculty

-- Add addresses
INSERT INTO addresses (person_id, address_type, address_line1, address_line2, city, state, postal_code, country, is_active) VALUES
(1, 'Work', '789 Admin Ave', NULL, 'Mumbai', 'Maharashtra', '400001', 'India', TRUE),
(2, 'Home', '123 Main St', NULL, 'Patna', 'Bihar', '800001', 'India', TRUE),
(3, 'Home', '456 College Rd', NULL, 'Delhi', 'Delhi', '110001', 'India', TRUE),
(4, 'Home', '12 Park Lane', NULL, 'Kolkata', 'West Bengal', '700001', 'India', TRUE),
(5, 'Home', '34 Lake View', NULL, 'Chennai', 'Tamil Nadu', '600001', 'India', TRUE);

-- Add contact_info
INSERT INTO contact_info (person_id, contact_type, contact_value, is_active) VALUES
(1, 'Email', 'admin@example.com', TRUE),
(1, 'Phone', '+91-9000000003', FALSE),
(2, 'Phone', '+91-9000000001', TRUE),
(2, 'Email', 'priya.ranjan@example.com', TRUE),
(3, 'Phone', '+91-9000000002', TRUE),
(3, 'Email', 'anita.sharma@example.com', TRUE),
(4, 'Phone', '+91-9000000004', TRUE),
(5, 'Email', 'sunita.devi@example.com', TRUE);
