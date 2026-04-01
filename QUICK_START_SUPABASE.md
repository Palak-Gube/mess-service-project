# ⚡ Quick Start - Supabase Database Setup

## 🎯 5-Minute Setup Guide

### **Step 1: Create Supabase Project (2 minutes)**

1. Go to **https://supabase.com**
2. Sign up/Login (free)
3. Click **"New Project"**
4. Fill in:
   - Name: `mess-service`
   - Password: (save this!)
   - Region: Choose closest
5. Click **"Create new project"**
6. Wait 2-3 minutes

---

### **Step 2: Get Credentials (1 minute)**

1. Go to **Project Settings** → **API**
2. Copy:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Go to **Database** → **Connection string**
4. Copy **Connection pooling URI**

---

### **Step 3: Set Environment Variables (1 minute)**

**Windows PowerShell:**
```powershell
$env:SUPABASE_URL="https://xxxxx.supabase.co"
$env:SUPABASE_KEY="eyJ..."
$env:SUPABASE_DB_PASSWORD="your-password"
$env:USE_SUPABASE="true"
```

**Or create `.env` file:**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_DB_PASSWORD=your-password
USE_SUPABASE=true
```

---

### **Step 4: Install Dependencies (30 seconds)**

```bash
cd micro_project_files
pip install -r requirements.txt
```

---

### **Step 5: Setup Database (1 minute)**

```bash
python supabase_setup.py
```

**This will:**
- ✅ Create all 8 tables
- ✅ Insert 100+ sample records
- ✅ Create admin user

**Expected output:**
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
...
🎉 Database setup complete!
```

---

### **Step 6: Start Flask (30 seconds)**

```bash
python app.py
```

---

### **Step 7: Test (30 seconds)**

1. Open browser: `http://localhost:5000`
2. Login as admin:
   - Username: `admin`
   - Password: `admin123`
3. Check admin dashboard:
   - ✅ Should show 100 students
   - ✅ Should show subscriptions
   - ✅ Should show feedbacks
   - ✅ Should show attendance

---

## ✅ Done!

Your database is now:
- ✅ Online (Supabase cloud)
- ✅ Has 100+ records
- ✅ All student actions save automatically
- ✅ Admin dashboard shows all data

---

## 🧪 Test Student Actions

1. **Register new student:**
   - Go to registration page
   - Fill form and submit
   - Check admin dashboard → User Management
   - ✅ New student appears!

2. **Mark attendance:**
   - Login as student
   - Click "Mark Breakfast"
   - Check admin dashboard → Attendance Report
   - ✅ Attendance appears!

3. **Submit feedback:**
   - Login as student
   - Submit feedback
   - Check admin dashboard → Feedbacks
   - ✅ Feedback appears!

4. **Select package:**
   - Login as student
   - Select a package
   - Check admin dashboard → Subscriptions
   - ✅ Subscription appears!

---

## 🎉 Everything Works!

All student actions are:
- ✅ Saved to database
- ✅ Visible in admin dashboard
- ✅ Update/delete operations work
- ✅ Real-time updates

**Your mess service is ready! 🚀**

