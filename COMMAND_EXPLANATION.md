# 📖 Command Explanation - What Each Step Does

## 🎯 Overview

These commands set up your database and start your Flask server. Let me explain each step:

---

## 📋 **Option 1: SQLite (Local Database)**

### **Step 1: `cd micro_project_files`**

**What it does:**
- Changes your current directory to the `micro_project_files` folder
- This is where all your project files are located

**Why needed:**
- All commands need to run from this folder
- Python files and database will be created here

**Example:**
```bash
# Before: You're in C:\Users\asus\Documents\GitHub\mess-service-microp
# After:  You're in C:\Users\asus\Documents\GitHub\mess-service-microp\micro_project_files
```

---

### **Step 2: `pip install -r requirements.txt`**

**What it does:**
- Installs all Python packages needed for the project
- Reads the `requirements.txt` file which lists all dependencies

**What gets installed:**
- Flask (web framework)
- Flask-SQLAlchemy (database)
- Flask-CORS (for frontend communication)
- Werkzeug (password hashing)
- Other dependencies

**Why needed:**
- Without these packages, Python can't run your Flask app
- First time setup only (unless you add new packages)

**Example output:**
```
Collecting Flask==3.1.2
  Downloading Flask-3.1.2-py3-none-any.whl
Installing collected packages: Flask, Flask-SQLAlchemy...
Successfully installed Flask-3.1.2 Flask-SQLAlchemy-3.1.1...
```

---

### **Step 3: `python supabase_setup.py`**

**What it does:**
- Creates your database file (`mess_service.db`)
- Creates all 8 database tables
- Inserts 100+ sample records (students, packages, attendance, etc.)

**What happens:**
1. Creates `mess_service.db` file (SQLite database)
2. Creates tables: users, students, admins, packages, subscriptions, attendance, feedbacks, menu_items
3. Inserts sample data:
   - 100 students
   - 5 packages
   - 50 subscriptions
   - 1000+ attendance records
   - 60 feedbacks
   - 10 menu items
   - 1 admin user

**Why needed:**
- Sets up your database structure
- Populates with test data so you can test immediately
- Only need to run once (unless you delete the database)

**Example output:**
```
📦 Using SQLite Database (Local)
✅ Database tables created!
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

**Result:**
- A file called `mess_service.db` is created in `micro_project_files` folder
- This file contains all your data

---

### **Step 4: `python app.py`**

**What it does:**
- Starts the Flask web server
- Makes your backend API available at `http://localhost:5000`
- Connects to your database
- Enables frontend to communicate with backend

**What happens:**
1. Flask server starts
2. Database connection established
3. API endpoints become available
4. Server runs until you stop it (Ctrl+C)

**Why needed:**
- Without this, your frontend can't talk to the backend
- Database operations won't work
- API endpoints won't be accessible

**Example output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**What you can do now:**
- Open `index.html` in browser
- Login as admin or student
- All features work (attendance, feedback, subscriptions, etc.)

**To stop server:**
- Press `Ctrl+C` in the terminal

---

## ☁️ **Option 2: Supabase (Cloud Database)**

### **Step 1: Create Supabase Project**

**What it means:**
- Go to https://supabase.com
- Sign up for free account
- Create a new project
- Get your project URL and API key

**Why needed:**
- Creates an online database (not local file)
- Database is accessible from anywhere
- Better for production/multiple users

**Result:**
- You get:
  - Project URL: `https://xxxxx.supabase.co`
  - API Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
  - Database password (you set this)

---

### **Step 2: Set Environment Variables**

**What it means:**
- Tell your computer where your Supabase database is
- Store your credentials securely

**Windows PowerShell:**
```powershell
$env:SUPABASE_URL="https://xxxxx.supabase.co"
$env:SUPABASE_KEY="eyJ..."
$env:SUPABASE_DB_PASSWORD="your-password"
$env:USE_SUPABASE="true"
```

**What each variable does:**
- `SUPABASE_URL` - Where your database is located
- `SUPABASE_KEY` - Your API key (like a password)
- `SUPABASE_DB_PASSWORD` - Database password
- `USE_SUPABASE` - Tells app to use Supabase instead of SQLite

**Why needed:**
- App needs to know which database to connect to
- Without these, it will use SQLite (local) instead

**Alternative: Create `.env` file**
Instead of typing commands, create a file named `.env` in `micro_project_files` folder:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_DB_PASSWORD=your-password
USE_SUPABASE=true
```

---

### **Step 3: `python supabase_setup.py`**

**What it does:**
- Same as SQLite version, but connects to Supabase instead
- Creates tables in your Supabase database
- Inserts 100+ sample records

**Difference from SQLite:**
- Data goes to cloud (Supabase) instead of local file
- You can see data in Supabase dashboard
- Database is online and accessible from anywhere

**Why needed:**
- Sets up your cloud database
- Populates with test data

---

### **Step 4: `python app.py`**

**What it does:**
- Same as SQLite version
- Starts Flask server
- Connects to Supabase database (instead of SQLite)

**Difference:**
- Connects to cloud database
- Data is stored online
- Can access from multiple devices

---

## 🔄 **Complete Flow Example**

### **SQLite (Local):**

```
1. cd micro_project_files
   → You're now in the project folder

2. pip install -r requirements.txt
   → Installing: Flask, Flask-SQLAlchemy, etc.
   → Takes 30-60 seconds

3. python supabase_setup.py
   → Creating: mess_service.db file
   → Creating: 8 tables
   → Inserting: 100 students, 50 subscriptions, etc.
   → Takes 10-30 seconds

4. python app.py
   → Starting Flask server
   → Server running on http://localhost:5000
   → Ready to use!
```

### **Supabase (Cloud):**

```
1. Create Supabase project (on website)
   → Get URL and API key

2. Set environment variables
   → Tell app where Supabase is

3. python supabase_setup.py
   → Creating tables in Supabase
   → Inserting data to cloud
   → Takes 30-60 seconds

4. python app.py
   → Starting Flask server
   → Connecting to Supabase
   → Ready to use!
```

---

## 📊 **What Happens Behind the Scenes**

### **When you run `python supabase_setup.py`:**

1. **Creates Database:**
   - SQLite: Creates `mess_service.db` file
   - Supabase: Creates tables in cloud

2. **Creates Tables:**
   ```
   users          → Login credentials
   students       → Student profiles
   admins         → Admin profiles
   packages       → Meal packages
   subscriptions  → Student subscriptions
   attendance     → Attendance records
   feedbacks     → Student feedbacks
   menu_items     → Menu items
   ```

3. **Inserts Sample Data:**
   - 100 students (can login)
   - 5 packages (can subscribe)
   - 50 subscriptions (billing data)
   - 1000+ attendance records
   - 60 feedbacks
   - 10 menu items
   - 1 admin (username: admin, password: admin123)

### **When you run `python app.py`:**

1. **Starts Flask Server:**
   - Listens on port 5000
   - Ready to receive requests

2. **Connects to Database:**
   - SQLite: Opens `mess_service.db` file
   - Supabase: Connects to cloud database

3. **Makes API Available:**
   - `/api/login` - Login endpoint
   - `/api/register` - Registration
   - `/api/students/<id>/attendance` - Mark attendance
   - `/api/admin/feedbacks` - Get feedbacks
   - And 20+ more endpoints

4. **Frontend Can Now:**
   - Login users
   - Save data to database
   - Retrieve data from database
   - Update/delete records

---

## ✅ **Quick Summary**

| Command | What It Does | When Needed |
|---------|-------------|-------------|
| `cd micro_project_files` | Go to project folder | Every time you open terminal |
| `pip install -r requirements.txt` | Install Python packages | First time only |
| `python supabase_setup.py` | Create database + sample data | First time only |
| `python app.py` | Start Flask server | Every time you want to use the app |

---

## 🎯 **Which Option to Choose?**

### **Choose SQLite if:**
- ✅ You're learning/developing
- ✅ You want it simple (no setup)
- ✅ You're working alone
- ✅ You don't need online access

### **Choose Supabase if:**
- ✅ You want online/cloud database
- ✅ Multiple people need access
- ✅ You want to deploy to production
- ✅ You want automatic backups

---

## 🚨 **Common Questions**

### **Q: Do I need to run all commands every time?**
**A:** No! Only:
- `cd micro_project_files` - Every time
- `python app.py` - Every time you want to use the app
- Others only once

### **Q: What if I delete the database?**
**A:** Just run `python supabase_setup.py` again to recreate it.

### **Q: Can I use both SQLite and Supabase?**
**A:** Yes! Set `USE_SUPABASE=false` for SQLite, `true` for Supabase.

### **Q: Where is my data stored?**
**A:** 
- SQLite: `micro_project_files/mess_service.db` file
- Supabase: In the cloud (see Supabase dashboard)

### **Q: How do I stop the server?**
**A:** Press `Ctrl+C` in the terminal where `python app.py` is running.

---

## 🎉 **That's It!**

Now you understand what each command does. Just follow the steps and your mess service will be ready to use!

