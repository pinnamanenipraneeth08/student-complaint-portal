-- Student Complaint Portal Database Schema

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS complaint_updates CASCADE;
DROP TABLE IF EXISTS attachments CASCADE;
DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- Departments Table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table (Students, Department Staff, Wardens, Admin)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'department', 'warden', 'admin')),
    registration_number VARCHAR(50),
    room_number VARCHAR(20),
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Complaints Table
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(20) NOT NULL UNIQUE,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    department_id INTEGER NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending' CHECK (status IN ('Pending', 'In Progress', 'Completed', 'Closed')),
    priority VARCHAR(50) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    expected_resolution_date DATE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complaint Updates (Replies and Status Updates)
CREATE TABLE complaint_updates (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    update_type VARCHAR(50) DEFAULT 'comment' CHECK (update_type IN ('comment', 'status_change', 'reply')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attachments Table
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_complaints_student ON complaints(student_id);
CREATE INDEX idx_complaints_department ON complaints(department_id);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_ticket ON complaints(ticket_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_complaint_updates_complaint ON complaint_updates(complaint_id);

-- Insert default departments
INSERT INTO departments (name, email, description) VALUES
    ('Food', 'food@klu.ac.in', 'Handles all food and mess related complaints'),
    ('Cleaning', 'cleaning@klu.ac.in', 'Handles cleaning and sanitation issues'),
    ('Electrical', 'electrical@klu.ac.in', 'Handles electrical repairs and maintenance'),
    ('Plumbing', 'plumbing@klu.ac.in', 'Handles plumbing and water supply issues'),
    ('Carpentry', 'carpentry@klu.ac.in', 'Handles furniture and carpentry work');

-- Insert default admin user (password: admin123)
INSERT INTO users (name, email, password_hash, role) VALUES
    ('Admin User', 'admin@klu.ac.in', 'scrypt:32768:8:1$hY9mZkxLXdHGFQQJ$ab4c7d8e9f0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567', 'admin');

-- Note: The password hash above is a placeholder. In the actual application,
-- use proper password hashing with werkzeug.security.generate_password_hash()
