# 🚀 Quick Start Guide - Student Complaint Portal

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] PostgreSQL 12 or higher installed and running
- [ ] Git (optional, for version control)
- [ ] A code editor (VS Code recommended)

---

## Step-by-Step Setup

### 1️⃣ Install PostgreSQL (if not installed)

**Windows:**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer and follow wizard
3. Remember your password for `postgres` user
4. Default port: 5432

**Mac (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2️⃣ Install Python Dependencies

Open terminal in project directory:

```bash
pip install -r requirements.txt
```

**If you get permission errors, use:**
```bash
pip install --user -r requirements.txt
```

### 3️⃣ Configure Database Connection

Edit `database/init_db.py` and update these lines (around line 8-12):

```python
conn = psycopg2.connect(
    host="localhost",
    user="postgres",           # Your PostgreSQL username
    password="your_password",  # Your PostgreSQL password
    database="postgres"
)
```

### 4️⃣ Initialize Database

Run the database setup script:

```bash
python database/init_db.py
```

**You should see:**
```
✅ Database 'student_portal' created successfully!
✅ Database schema initialized successfully!
✅ Default departments created
✅ Default admin user created
```

**If you see errors:**
- Check PostgreSQL is running: `psql --version`
- Verify credentials in init_db.py
- Ensure PostgreSQL service is started

### 5️⃣ Create Environment File

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and update:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/student_portal
   SECRET_KEY=change-this-to-random-secret-key
   ```

3. Generate a strong secret key (Python):
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

### 6️⃣ Run the Application

```bash
python app.py
```

**You should see:**
```
====================================================
🎓 Student Complaint Portal
====================================================
🌐 Server running at: http://localhost:5000
📧 Default Admin: admin@klu.ac.in / admin123
====================================================
```

### 7️⃣ Access the Portal

Open your browser and go to: **http://localhost:5000**

---

## 🎯 First Steps After Setup

### 1. Login as Admin
- Email: `admin@klu.ac.in`
- Password: `admin123`
- **⚠️ Change password immediately!**

### 2. Create Department Users
1. Go to **Admin Dashboard** → **Users** → **Create New User**
2. Create users for each department:
   - Food Department
   - Cleaning Department
   - Electrical Department
   - Plumbing Department
   - Carpentry Department

### 3. Test Student Registration
1. Logout
2. Click **Register**
3. Use a `@klu.ac.in` email address
4. Fill in student details
5. Submit complaint

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "psycopg2.OperationalError: could not connect to server"
**Solution:** 
1. Check if PostgreSQL is running
2. Verify credentials in `init_db.py`
3. Try: `psql -U postgres` in terminal

### Problem: "Database 'student_portal' already exists"
**Solution:** This is normal! Database already created.

### Problem: "ImportError: cannot import name 'db'"
**Solution:** Make sure all files are created correctly. Run:
```bash
python -c "from models import db; print('OK')"
```

### Problem: Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: File upload not working
**Solution:** Check `static/uploads/` directory exists with write permissions

---

## 📊 Testing the System

### Test Scenario 1: Student Flow
1. Register as student with `@klu.ac.in` email
2. Login
3. Submit a complaint to "Food" department
4. Upload an image
5. Check dashboard for ticket ID

### Test Scenario 2: Department Flow
1. Login as admin
2. Create a "Food Department" user
3. Logout, login as that user
4. View the student's complaint
5. Reply and change status to "In Progress"
6. Set expected resolution date

### Test Scenario 3: Admin Flow
1. Login as admin
2. View all complaints across departments
3. Check department-wise statistics
4. View long-pending complaints
5. Generate reports

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change admin password from default
- [ ] Generate new SECRET_KEY
- [ ] Update DATABASE_URL with production credentials
- [ ] Set `FLASK_ENV=production` in .env
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Implement rate limiting
- [ ] Add email verification

---

## 📈 Performance Tips

1. **For Production:**
   - Use Gunicorn: `pip install gunicorn`
   - Run: `gunicorn -w 4 app:app`

2. **Database Optimization:**
   - Enable connection pooling
   - Add database indexes (already included in schema)
   - Regular VACUUM on PostgreSQL

3. **File Storage:**
   - Move uploads to cloud storage (AWS S3, Azure Blob)
   - Implement CDN for static files

---

## 🎓 Usage Tips

### For Students:
- Use clear, descriptive subjects
- Provide detailed descriptions
- Upload evidence (photos/videos)
- Check dashboard regularly for updates
- Reply to department queries promptly

### For Departments:
- Respond within 24 hours
- Update status regularly
- Set realistic resolution dates
- Close completed complaints
- Maintain professional communication

### For Admin:
- Monitor pending complaints daily
- Escalate long-pending issues
- Review department performance
- Generate weekly reports
- Keep user accounts updated

---

## 📞 Need Help?

If you encounter issues:

1. Check this guide first
2. Review error messages carefully
3. Check logs in terminal
4. Verify all files are present
5. Ensure dependencies are installed

---

## 🎉 Success!

If everything is working:
- ✅ You can access the portal at localhost:5000
- ✅ Admin login works
- ✅ Students can register
- ✅ Complaints can be submitted
- ✅ Departments can respond
- ✅ Files upload successfully

**Congratulations! Your Student Complaint Portal is ready! 🎊**

---

**Next Steps:** Customize the portal with your university branding, colors, and logo!
