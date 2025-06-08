-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS student_mgmt;
USE student_mgmt;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    salted_password VARCHAR(255) NOT NULL
);

-- Create user_roles table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Insert default roles only if they don't exist
INSERT IGNORE INTO roles (id, name) VALUES
(1, 'Administrator'),
(2, 'Faculty'),
(3, 'Student');

-- Insert default users only if they don't exist
INSERT IGNORE INTO users (id, username, salted_password) VALUES
(1, 'admin', SHA2(CONCAT('password123','admin_salt'),256)),
(2, 'student', SHA2(CONCAT('password123','student_salt'),256)),
(3, 'faculty', SHA2(CONCAT('password123','faculty_salt'),256));

-- Insert user-role mappings only if they don't exist
INSERT IGNORE INTO user_roles (user_id, role_id) VALUES
(1, 1), -- admin
(2, 3), -- student
(3, 2); -- faculty
