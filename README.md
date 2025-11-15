# Student Complaint Portal

A comprehensive web-based grievance management system designed for university hostels.

## 🎓 Project Overview

The **Student Complaint Portal** provides a streamlined platform where students can raise complaints, departments can respond and resolve issues, and admins can monitor overall progress. The system ensures transparency, accountability, and faster resolution of hostel-related problems.

## ✨ Key Features

### For Students
- 📧 Secure login using university email (@klu.ac.in)
- 📝 Submit complaints with file attachments (images/videos)
- 🎫 Auto-generated unique Ticket ID
- 📊 Real-time status tracking
- 💬 Reply to department updates
- 📱 Mobile-responsive interface

### For Departments/Wardens
- 🔍 View complaints filtered by department
- 💬 Reply to student complaints
- ⚡ Update complaint status (Pending → In Progress → Completed)
- 📅 Set expected resolution dates
- 🏷️ Manage complaint priorities

### For Admin
- 🔭 System-wide complaint monitoring
- 📈 Department-wise statistics
- 👥 User management (create department accounts)
- ⚠️ Track long-pending complaints
- 📊 Reports and analytics

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Authentication:** Email-based with Flask-Login
- **File Storage:** Local storage (scalable to cloud)

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
cd student_portal
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

Make sure PostgreSQL is installed and running, then:

```bash
# Update database credentials in database/init_db.py if needed
python database/init_db.py
```

This will:
- Create the `student_portal` database
- Set up all tables and relationships
- Insert default departments
- Create default admin user

### 4. Configure Environment Variables

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and update:
```
DATABASE_URL=postgresql://postgres:your_password@localhost/student_portal
SECRET_KEY=your-secret-key-here
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 👤 Default Credentials

**Admin Login:**
- Email: `admin@klu.ac.in`
- Password: `admin123`

**Note:** Change the admin password after first login!

## 📁 Project Structure

```
student_portal/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── database/
│   ├── schema.sql         # Database schema
│   └── init_db.py         # Database initialization
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── complaint.py
│   └── department.py
├── routes/                # Flask blueprints/routes
│   ├── auth.py           # Authentication
│   ├── student.py        # Student routes
│   ├── department.py     # Department routes
│   └── admin.py          # Admin routes
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student/
│   ├── department/
│   ├── admin/
│   └── errors/
└── static/                # CSS, JS, uploads
    ├── css/
    ├── js/
    └── uploads/
```

## 🔄 Workflow

1. **Student** → Submit Complaint
2. **System** → Generate Ticket ID
3. **System** → Forward to Department
4. **Department** → Respond & Update Status
5. **Student** → Track Progress
6. **Admin** → Monitor & Escalate if needed

## 📊 Database Schema

### Main Tables:
- **users** - All user accounts (students, departments, admin)
- **departments** - 5 departments (Food, Cleaning, Electrical, Plumbing, Carpentry)
- **complaints** - All complaint tickets
- **complaint_updates** - Conversation history
- **attachments** - Uploaded files

## 🔐 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- File upload validation
- Role-based access control
- University email verification for students

## 📱 Mobile Responsive

The portal is fully responsive and works seamlessly on:
- 💻 Desktop
- 📱 Mobile
- 📱 Tablet

## 🎨 UI/UX Features

- Clean, modern Bootstrap 5 design
- Color-coded status indicators
- Real-time status timeline
- Font Awesome icons
- Smooth animations
- Alert notifications

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is developed for educational purposes.

## 👨‍💻 Developer

**Your Name**  
KL University  
📧 Contact: your.email@klu.ac.in

## 🐛 Bug Reports

Found a bug? Please create an issue with:
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## 🎯 Future Enhancements

- [ ] Email notifications
- [ ] SMS alerts
- [ ] Mobile app
- [ ] AI-powered complaint categorization
- [ ] Analytics dashboard
- [ ] Feedback system
- [ ] Cloud storage integration

## 📞 Support

For support, contact the admin or raise an issue in the repository.

---

**Made with ❤️ for KL University Students**
