# Mess Service Backend - Setup Guide

## 📁 Database Structure

**Single Database Approach** (Recommended)
- **Database File**: `mess_service.db` (SQLite)
- **All tables in one database** for easier management

### Tables Created:
1. **users** - Login credentials (students & admins)
2. **students** - Student details
3. **admins** - Admin details
4. **feedbacks** - All student feedbacks
5. **packages** - Available meal packages
6. **subscriptions** - Student meal subscriptions
7. **attendance** - Daily meal attendance
8. **menu_items** - Daily menu items

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python init_db.py
```
This creates:
- All database tables
- Sample packages (Basic Daily, Premium Weekly, VIP Monthly)
- Sample admin (username: `admin`, password: `admin123`)
- Sample student (username: `student1`, password: `student123`)

### Step 3: Run Flask Server
```bash
python app.py
```
Server runs on: `http://localhost:5000`

## 📡 API Endpoints

### Authentication
- `POST /api/login` - Login (student/admin)
- `POST /api/register` - Register new user

### Student Endpoints
- `GET /api/students/<id>` - Get student profile
- `PUT /api/students/<id>` - Update profile
- `POST /api/students/<id>/feedback` - Submit feedback
- `GET /api/students/<id>/subscriptions` - Get subscriptions
- `POST /api/students/<id>/subscriptions` - Select package
- `POST /api/students/<id>/attendance` - Mark attendance
- `GET /api/students/<id>/attendance` - Get attendance

### Admin Endpoints
- `GET /api/admin/feedbacks` - View all feedbacks
- `GET /api/admin/subscriptions` - View all subscriptions
- `POST /api/admin/attendance` - Mark student attendance
- `GET /api/admin/attendance` - Get attendance report
- `GET /api/admin/dashboard` - Dashboard statistics

### Menu & Packages
- `GET /api/menu/today` - Get today's menu
- `GET /api/packages` - Get all packages

## 💻 Frontend Integration

### Using the API Utility (`api.js`)

**Login:**
```javascript
const result = await auth.login('student', 'username', 'password');
```

**Submit Feedback:**
```javascript
const result = await student.submitFeedback(userId, 'Great food!');
```

**Select Package:**
```javascript
const result = await student.selectPackage(userId, packageId);
```

**Admin - View Feedbacks:**
```javascript
const feedbacks = await admin.getAllFeedbacks();
```

All API calls are centralized in `api.js` - no need for long JavaScript code!

## 🔧 Configuration

- **Database**: SQLite (`mess_service.db`)
- **Port**: 5000
- **CORS**: Add CORS if needed for cross-origin requests

## 📝 Notes

- Passwords are hashed using Werkzeug
- All dates stored as ISO format
- Unique constraints prevent duplicate attendance records
- Relationships properly set up with foreign keys

