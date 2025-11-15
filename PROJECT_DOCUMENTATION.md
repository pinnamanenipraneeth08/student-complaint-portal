# 🎓 Student Complaint Portal - Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Features & Modules](#features--modules)
4. [Technology Stack](#technology-stack)
5. [Database Design](#database-design)
6. [User Roles & Permissions](#user-roles--permissions)
7. [Installation Guide](#installation-guide)
8. [Testing Scenarios](#testing-scenarios)
9. [Screenshots](#screenshots)
10. [Future Enhancements](#future-enhancements)

---

## 📌 Project Overview

### Purpose
The Student Complaint Portal is a comprehensive web-based grievance management system designed specifically for university hostel environments. It streamlines the process of complaint submission, tracking, and resolution, ensuring transparency and accountability.

### Problem Statement
Traditional hostel complaint management faces several challenges:
- Manual tracking leads to lost complaints
- No transparency in resolution process
- Delayed responses from departments
- Lack of accountability
- Poor communication between students and departments
- No data for analysis and improvement

### Solution
A digital platform that:
- ✅ Automates complaint tracking with unique ticket IDs
- ✅ Provides real-time status updates
- ✅ Enables direct communication between stakeholders
- ✅ Offers analytics for administrators
- ✅ Ensures accountability through audit trails
- ✅ Improves response times and resolution rates

---

## 🏗️ System Architecture

### Architecture Type
**Three-Tier Architecture**

```
┌─────────────────────────────────────┐
│     Presentation Layer (Frontend)   │
│   HTML5, CSS3, Bootstrap, JavaScript│
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Application Layer (Backend)    │
│      Flask, Python, Flask-Login     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Data Layer (Database)         │
│       PostgreSQL, SQLAlchemy        │
└─────────────────────────────────────┘
```

### Component Breakdown

**Frontend Components:**
- Login/Registration Pages
- Student Dashboard
- Department Dashboard
- Admin Dashboard
- Complaint Forms
- Status Tracking Interface

**Backend Components:**
- Authentication Module (`routes/auth.py`)
- Student Module (`routes/student.py`)
- Department Module (`routes/department.py`)
- Admin Module (`routes/admin.py`)
- Database Models (`models/`)
- File Upload Handler

**Database Components:**
- User Management
- Complaint Tracking
- Department Management
- Audit Logs
- File Attachments

---

## ✨ Features & Modules

### 1. Student Module

**Features:**
- ✅ University email-based registration (@klu.ac.in)
- ✅ Secure login with password hashing
- ✅ Submit complaints with details:
  - Subject
  - Description
  - Department selection
  - Priority level
  - File attachments (images/videos)
- ✅ Auto-generated unique Ticket ID (Format: TCK-YYYYMMDD-XXXX)
- ✅ Real-time complaint tracking
- ✅ View all submitted complaints
- ✅ Filter by status and department
- ✅ Reply to department updates
- ✅ View conversation history

**Workflow:**
1. Student registers with university email
2. Login with credentials
3. Submit complaint with details
4. Receive unique ticket ID
5. Track status in real-time
6. Receive updates from department
7. Reply to department queries
8. Complaint marked as completed

### 2. Department/Warden Module

**Features:**
- ✅ Department-specific login
- ✅ View complaints assigned to department
- ✅ Filter by status and priority
- ✅ View complete complaint details
- ✅ Access student information
- ✅ Reply to complaints
- ✅ Update complaint status:
  - Pending
  - In Progress
  - Completed
- ✅ Set expected resolution date
- ✅ Adjust priority levels
- ✅ View conversation history

**Workflow:**
1. Department user logs in
2. Views assigned complaints
3. Reviews complaint details and attachments
4. Responds to student
5. Updates status to "In Progress"
6. Sets expected resolution date
7. Works on issue
8. Updates status to "Completed"
9. Adds final resolution notes

### 3. Admin Module

**Features:**
- ✅ System-wide dashboard
- ✅ View all complaints across departments
- ✅ Department-wise statistics:
  - Total complaints per department
  - Pending count
  - Completed count
  - Completion rate
- ✅ Identify long-pending complaints (7+ days)
- ✅ User management:
  - Create department users
  - Activate/deactivate users
  - View user details
- ✅ Reports and analytics:
  - 30-day complaint trends
  - Average resolution time
  - Priority distribution
- ✅ Filter and search capabilities
- ✅ Escalation management

**Workflow:**
1. Admin logs in
2. Reviews system-wide statistics
3. Monitors department performance
4. Identifies bottlenecks
5. Creates department user accounts
6. Escalates long-pending complaints
7. Generates reports
8. Takes corrective actions

---

## 🛠️ Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM for database |
| Flask-Login | 0.6.3 | User session management |
| psycopg2 | 2.9.9 | PostgreSQL adapter |
| Werkzeug | 3.0.1 | Password hashing |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Structure |
| CSS3 | - | Styling |
| Bootstrap | 5.3.0 | Responsive framework |
| JavaScript | ES6 | Interactivity |
| Font Awesome | 6.4.0 | Icons |

### Database
| Technology | Version | Purpose |
|------------|---------|---------|
| PostgreSQL | 12+ | Relational database |

### Development Tools
- VS Code (Code editor)
- Git (Version control)
- pgAdmin (Database management)

---

## 🗄️ Database Design

### Entity-Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  DEPARTMENTS │       │    USERS     │       │  COMPLAINTS  │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │◄──────│ id (PK)      │──────►│ id (PK)      │
│ name         │       │ name         │       │ ticket_id    │
│ email        │       │ email        │       │ student_id(FK)│
│ description  │       │ password_hash│       │ dept_id (FK) │
└──────────────┘       │ role         │       │ subject      │
                       │ reg_number   │       │ description  │
                       │ room_number  │       │ status       │
                       │ dept_id (FK) │       │ priority     │
                       └──────────────┘       │ created_at   │
                                              └──────┬───────┘
                                                     │
                        ┌────────────────────────────┼────────────────────┐
                        │                            │                    │
                  ┌─────▼─────┐            ┌────────▼────────┐  ┌────────▼────────┐
                  │ATTACHMENTS│            │COMPLAINT_UPDATES│  │                 │
                  ├───────────┤            ├─────────────────┤  │                 │
                  │ id (PK)   │            │ id (PK)         │  │                 │
                  │ complaint │            │ complaint_id(FK)│  │                 │
                  │ file_name │            │ user_id (FK)    │  │                 │
                  │ file_path │            │ message         │  │                 │
                  └───────────┘            │ update_type     │  │                 │
                                           └─────────────────┘  └─────────────────┘
```

### Table Schemas

#### 1. DEPARTMENTS
```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Data:**
- Food
- Cleaning
- Electrical
- Plumbing
- Carpentry

#### 2. USERS
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'department', 'warden', 'admin')),
    registration_number VARCHAR(50),
    room_number VARCHAR(20),
    department_id INTEGER REFERENCES departments(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### 3. COMPLAINTS
```sql
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(20) NOT NULL UNIQUE,
    student_id INTEGER NOT NULL REFERENCES users(id),
    department_id INTEGER NOT NULL REFERENCES departments(id),
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    priority VARCHAR(50) DEFAULT 'Medium',
    expected_resolution_date DATE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. COMPLAINT_UPDATES
```sql
CREATE TABLE complaint_updates (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES complaints(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    message TEXT NOT NULL,
    update_type VARCHAR(50) DEFAULT 'comment',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. ATTACHMENTS
```sql
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES complaints(id),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 👥 User Roles & Permissions

### Role Matrix

| Feature | Student | Department | Warden | Admin |
|---------|---------|------------|--------|-------|
| Register | ✅ | ❌ | ❌ | ❌ |
| Submit Complaint | ✅ | ❌ | ❌ | ❌ |
| View Own Complaints | ✅ | ❌ | ❌ | ❌ |
| View Dept Complaints | ❌ | ✅ | ✅ | ✅ |
| Reply to Complaints | ✅ | ✅ | ✅ | ✅ |
| Update Status | ❌ | ✅ | ✅ | ✅ |
| Set Priority | ❌ | ✅ | ✅ | ✅ |
| View All Complaints | ❌ | ❌ | ❌ | ✅ |
| Create Users | ❌ | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ❌ | ✅ |
| View Reports | ❌ | ❌ | ❌ | ✅ |

---

## 📦 Installation Guide

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation instructions.

**Quick Start:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python database/init_db.py

# 3. Run application
python app.py
```

---

## 🧪 Testing Scenarios

### Test Case 1: Student Registration
**Steps:**
1. Go to registration page
2. Enter name: "John Doe"
3. Enter email: "john.doe@klu.ac.in"
4. Enter registration: "2100030123"
5. Enter room: "A-301"
6. Set password
7. Submit

**Expected:** Registration successful, redirect to login

### Test Case 2: Complaint Submission
**Steps:**
1. Login as student
2. Click "Submit Complaint"
3. Select "Food" department
4. Enter subject: "Poor food quality"
5. Describe issue
6. Upload photo
7. Submit

**Expected:** Ticket ID generated, complaint visible in dashboard

### Test Case 3: Department Response
**Steps:**
1. Login as Food department user
2. View complaint list
3. Open student's complaint
4. Reply with message
5. Update status to "In Progress"
6. Set expected date

**Expected:** Status updated, student sees update

---

## 🚀 Future Enhancements

### Phase 2 Features
1. **Email Notifications**
   - Complaint submission confirmation
   - Status update alerts
   - Daily digest for departments

2. **SMS Integration**
   - Critical complaint alerts
   - Resolution notifications

3. **Mobile Application**
   - Native Android/iOS apps
   - Push notifications
   - Quick complaint submission

4. **Advanced Analytics**
   - Trend analysis
   - Predictive analytics
   - Department performance metrics

5. **AI Integration**
   - Auto-categorization
   - Sentiment analysis
   - Suggested resolutions

6. **Feedback System**
   - Post-resolution rating
   - Department feedback
   - Service quality metrics

7. **Multi-language Support**
   - Regional languages
   - International students

8. **Cloud Integration**
   - AWS S3 for file storage
   - Azure deployment
   - CDN for static assets

---

## 📊 Project Statistics

- **Total Files:** 35+
- **Lines of Code:** 3000+
- **Database Tables:** 5
- **User Roles:** 4
- **Departments:** 5
- **Features:** 30+

---

## 📝 Conclusion

The Student Complaint Portal successfully addresses the challenges of traditional hostel grievance management by providing:
- ✅ Streamlined complaint submission
- ✅ Real-time tracking
- ✅ Transparent communication
- ✅ Accountability at all levels
- ✅ Data-driven insights for improvement

This system can be easily customized and scaled for:
- Different educational institutions
- Corporate environments
- Government offices
- Community management

---

**Developed for KL University Students** 🎓  
**Version:** 1.0.0  
**Last Updated:** November 2025
