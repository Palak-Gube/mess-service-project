# 🚀 Supabase Database Setup Guide

## 📋 Overview

This guide will help you:
1. ✅ Set up Supabase database (online/cloud)
2. ✅ Create all 8 tables with proper relationships
3. ✅ Populate with 100+ sample records
4. ✅ Connect Flask app to Supabase
5. ✅ Ensure all student actions save to database
6. ✅ Show all data in admin dashboard

---

## 🎯 Step 1: Create Supabase Project

1. **Go to https://supabase.com**
2. **Sign up/Login** (free account)
3. **Click "New Project"**
4. **Fill in:**
   - Project Name: `mess-service`
   - Database Password: (choose a strong password - **SAVE THIS!**)
   - Region: Choose closest to you
5. **Click "Create new project"**
6. **Wait 2-3 minutes** for project to initialize

---

## 🔑 Step 2: Get API Credentials

1. **Go to Project Settings** (gear icon)
2. **Click "API"** in left sidebar
3. **Copy these values:**
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (long string starting with `eyJ...`)

4. **Click "Database"** in left sidebar
5. **Find "Connection string"** section
6. **Copy "Connection pooling" URI** (starts with `postgresql://`)

---

## 📝 Step 3: Set Environment Variables

### **Windows PowerShell:**
```powershell
$env:SUPABASE_URL="https://xxxxx.supabase.co"
$env:SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
$env:SUPABASE_DB_PASSWORD="your-database-password"
$env:USE_SUPABASE="true"
```

### **Windows Command Prompt:**
```cmd
set SUPABASE_URL=https://xxxxx.supabase.co
set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
set SUPABASE_DB_PASSWORD=your-database-password
set USE_SUPABASE=true
```

### **Linux/Mac:**
```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
export SUPABASE_DB_PASSWORD="your-database-password"
export USE_SUPABASE="true"
```

### **Or Create .env File:**
Create `micro_project_files/.env`:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_DB_PASSWORD=your-database-password
USE_SUPABASE=true
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

And add to `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🗄️ Step 4: Create Database Tables

### **Option A: Using Supabase SQL Editor (Recommended)**

1. **Go to SQL Editor** in Supabase dashboard
2. **Click "New query"**
3. **Copy and paste** the SQL from `supabase_setup.py` (function `create_tables_sql()`)
4. **Click "Run"**
5. **Verify tables created** in "Table Editor"

### **Option B: Using Python Script**

```bash
cd micro_project_files
python supabase_setup.py
```

This will:
- ✅ Create all 8 tables
- ✅ Add indexes for performance
- ✅ Set up foreign key relationships

---

## 📥 Step 5: Populate with 100+ Records

Run the setup script:

```bash
cd micro_project_files
python supabase_setup.py
```

**What it does:**
- ✅ Creates 100 students with unique usernames
- ✅ Creates 5 meal packages
- ✅ Creates 50 subscriptions
- ✅ Creates 1000+ attendance records (last 30 days)
- ✅ Creates 60 feedbacks
- ✅ Creates 10 menu items
- ✅ Creates admin user (username: `admin`, password: `admin123`)

**Expected Output:**
```
🚀 Setting up Supabase Database...
☁️  Using Supabase Database (Cloud)
✅ Connected to Supabase!
📝 Generating sample data...
✅ Generated:
   - 100 users
   - 100 students
   - 5 packages
   - 50 subscriptions
   - 1000+ attendance records
   - 60 feedbacks
   - 10 menu items
📥 Inserting users and students...
✅ Inserted 100 students!
...
🎉 Database setup complete!
```

---

## 🔌 Step 6: Update Flask App

The `app.py` is already configured to:
- ✅ Auto-detect Supabase if environment variables are set
- ✅ Fall back to SQLite if Supabase not configured
- ✅ Support both databases seamlessly

**No code changes needed!** Just set environment variables.

---

## ✅ Step 7: Verify Setup

### **1. Check Database Connection:**
```bash
python -c "from app import app, db; app.app_context().push(); print('✅ Database connected!')"
```

### **2. Check Record Counts:**
```bash
python -c "from app import app, db, Student; app.app_context().push(); print(f'Students: {Student.query.count()}')"
```

### **3. Start Flask:**
```bash
python app.py
```

### **4. Test Login:**
- Admin: username=`admin`, password=`admin123`
- Student: username=`student1`, password=`password123`

### **5. Check Admin Dashboard:**
- Should show 100 students
- Should show all subscriptions
- Should show all feedbacks
- Should show attendance records

---

## 🔄 Data Flow: Student Actions → Database → Admin Dashboard

### **How It Works:**

1. **Student marks attendance:**
   ```
   Student Dashboard → POST /api/students/<id>/attendance
   → Saves to `attendance` table
   → Admin Dashboard → GET /api/admin/attendance
   → Shows in admin dashboard ✅
   ```

2. **Student submits feedback:**
   ```
   Student Dashboard → POST /api/students/<id>/feedback
   → Saves to `feedbacks` table
   → Admin Dashboard → GET /api/admin/feedbacks
   → Shows in admin dashboard ✅
   ```

3. **Student selects package:**
   ```
   Student Dashboard → POST /api/students/<id>/subscriptions
   → Saves to `subscriptions` table
   → Admin Dashboard → GET /api/admin/subscriptions
   → Shows in admin dashboard ✅
   ```

4. **Student registers:**
   ```
   Registration → POST /api/register
   → Saves to `users` and `students` tables
   → Admin Dashboard → GET /api/admin/students
   → Shows in admin dashboard ✅
   ```

**All actions are automatically saved and visible!**

---

## 🗑️ Update & Delete Operations

### **Update Operations:**

All update endpoints save changes immediately:

- ✅ `PUT /api/students/<id>` - Update student profile
- ✅ `PUT /api/admin/menu/<id>` - Update menu item
- ✅ `PUT /api/admin/attendance/<id>` - Update attendance
- ✅ `PUT /api/admin/subscriptions/<id>` - Update subscription status

### **Delete Operations:**

All delete endpoints remove from database:

- ✅ `DELETE /api/admin/menu/<id>` - Delete menu item
- ✅ `DELETE /api/admin/attendance/<id>` - Delete attendance record

**Changes are immediately reflected in dashboards!**

---

## 📊 Database Schema

### **8 Tables:**

1. **users** - Authentication (login/register)
2. **students** - Student profiles
3. **admins** - Admin profiles
4. **packages** - Meal packages
5. **subscriptions** - Student subscriptions (billing)
6. **attendance** - Meal attendance records
7. **feedbacks** - Student feedbacks
8. **menu_items** - Menu items

### **Relationships:**

- `users` → `students` (1:1)
- `users` → `admins` (1:1)
- `students` → `subscriptions` (1:many)
- `students` → `attendance` (1:many)
- `students` → `feedbacks` (1:many)
- `packages` → `subscriptions` (1:many)

---

## 🔍 Verify in Supabase Dashboard

1. **Go to Table Editor** in Supabase
2. **Click on each table** to see data:
   - `users` - Should have 101 rows (100 students + 1 admin)
   - `students` - Should have 100 rows
   - `subscriptions` - Should have 50 rows
   - `attendance` - Should have 1000+ rows
   - `feedbacks` - Should have 60 rows
   - `menu_items` - Should have 10 rows

---

## 🐛 Troubleshooting

### **"Connection refused"**
- Check SUPABASE_URL is correct
- Check SUPABASE_KEY is correct
- Verify project is active in Supabase dashboard

### **"Authentication failed"**
- Check SUPABASE_DB_PASSWORD is correct
- Reset password in Supabase if needed

### **"Table does not exist"**
- Run SQL script in Supabase SQL Editor
- Or run `supabase_setup.py`

### **"No data showing"**
- Check environment variables are set
- Restart Flask server after setting variables
- Verify data exists in Supabase Table Editor

---

## ✅ Success Checklist

- [ ] Supabase project created
- [ ] Environment variables set
- [ ] Tables created (8 tables)
- [ ] 100+ records inserted
- [ ] Flask connects to Supabase
- [ ] Can login as admin/student
- [ ] Admin dashboard shows all data
- [ ] Student actions save to database
- [ ] Update/delete operations work

---

## 🎉 You're Done!

Your database is now:
- ✅ Online (Supabase cloud)
- ✅ Has 100+ records
- ✅ All student actions save automatically
- ✅ Admin dashboard shows all data
- ✅ Update/delete operations work

**Start using:**
```bash
python app.py
```

---

## 📞 Need Help?

- Check Supabase logs in dashboard
- Check Flask terminal for errors
- Verify environment variables
- Check database connection in Supabase

**Your mess service is now fully connected to Supabase! 🚀**

