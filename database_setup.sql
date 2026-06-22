CREATE DATABASE resume_management;

USE resume_management;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE candidates (

    candidate_id INT AUTO_INCREMENT PRIMARY KEY,

    candidate_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone_number VARCHAR(20),

    education TEXT,
    experience VARCHAR(50),

    current_company VARCHAR(255),
    current_designation VARCHAR(255),
    current_location VARCHAR(255),

    resume_path VARCHAR(500) NOT NULL,

    status ENUM(
        'SAVED',
        'INTERVIEW_SCHEDULED',
        'ON_HOLD',
        'SELECTED',
        'REJECTED'
    ) NOT NULL DEFAULT 'SAVED',

    interview_date DATE NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

);

-- Sample Admin Account
INSERT INTO users(username, password)
VALUES ('admin', 'admin123');