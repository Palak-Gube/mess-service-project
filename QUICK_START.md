# 🚀 Quick Start Guide - Complete Setup

## Step-by-Step Setup (5 Minutes)

### 1️⃣ Open Terminal/Command Prompt
Navigate to the project folder:
```bash
cd micro_project_files
```

### 2️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

**This installs:**
- Flask (web framework)
- Flask-SQLAlchemy (database)
- Flask-CORS (for frontend communication)
- Werkzeug (password hashing)

### 3️⃣ Create Database (One-Time Setup)
```bash
python init_db.py
```

**What happens:**
- ✅ Creates `mess_service.db` file automatically
- ✅ Creates all 8 database tables
- ✅ Adds sample data (packages, admin, student)

**Expected output:**
```
✅ Database tables created!
✅ Sample packages added!
✅ Sample admin created! (username: admin, password: admin123)
✅ Sample student created! (username: student1, password: student123)

🎉 Database initialized successfully!
```

### 4️⃣ Start Flask Server
```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 5️⃣ Open Frontend
- Open `index.html` in your web browser
- Or use a local server (optional)

### 6️⃣ Test Login

**Admin Login:**
- Username: `admin`
- Password: `admin123`
- Role: Select "Mess Admin/Staff"

**Student Login:**
- Username: `student1`
- Password: `student123`
- Role: Select "Student/Resident"

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] Database file `mess_service.db` exists
- [ ] Flask server running on port 5000
- [ ] Can login as admin
- [ ] Can login as student
- [ ] Dashboard shows data

## 🎯 You're Ready!

The database is now set up and ready to use. All data will be saved automatically in `mess_service.db`.

---

## 📁 File Structure

```
micro_project_files/
├── app.py              ← Flask backend
├── init_db.py          ← Database setup script
├── mess_service.db     ← Database file (created automatically)
├── api.js              ← Frontend API utility
├── index.html          ← Landing page
└── ... (other HTML files)
```

## 🔧 Common Issues

**Issue:** "No module named 'flask'"
- **Solution:** Run `pip install -r requirements.txt`

**Issue:** "Database file not found"
- **Solution:** Run `python init_db.py` first

**Issue:** "Port 5000 already in use"
- **Solution:** Change port in `app.py` or close other application using port 5000

---

**That's it! Your database is ready! 🎉**

