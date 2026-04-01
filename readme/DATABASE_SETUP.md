# Database Setup Guide

## 📊 About SQLite Database

**Good News!** You don't need to manually create a SQLite database. SQLite automatically creates the database file when you run the application.

## 🚀 How to Set Up the Database

### Step 1: Install Dependencies
```bash
cd micro_project_files
pip install -r requirements.txt
```

### Step 2: Initialize Database
Run this command to create the database and all tables:

```bash
python init_db.py
```

**What this does:**
- ✅ Creates `mess_service.db` file (automatically)
- ✅ Creates all 8 database tables
- ✅ Adds sample meal packages
- ✅ Creates sample admin account
- ✅ Creates sample student account

### Step 3: Verify Database Created
After running `init_db.py`, you should see:
- A new file: `mess_service.db` in the `micro_project_files` folder
- Success messages in the terminal

## 📁 Database File Location

The database file will be created at:
```
micro_project_files/mess_service.db
```

## 🗄️ Database Structure

The database contains **8 tables**:

1. **users** - Login credentials
2. **students** - Student details
3. **admins** - Admin details
4. **feedbacks** - Student feedbacks
5. **packages** - Meal packages
6. **subscriptions** - Student subscriptions
7. **attendance** - Daily attendance
8. **menu_items** - Menu items

## 🔑 Default Login Credentials

After running `init_db.py`, you can login with:

**Admin:**
- Username: `admin`
- Password: `admin123`

**Student:**
- Username: `student1`
- Password: `student123`

## ⚠️ Important Notes

1. **Database is created automatically** - No need to manually create it
2. **First time setup** - Run `init_db.py` once to initialize
3. **Database file** - `mess_service.db` will appear after first run
4. **Data persistence** - All data is saved in the `.db` file
5. **No SQL knowledge needed** - Everything is handled by Flask-SQLAlchemy

## 🔄 Re-initializing Database

If you want to start fresh (delete all data):

1. Delete `mess_service.db` file
2. Run `python init_db.py` again

## 📝 Troubleshooting

### Database file not created?
- Make sure you're in the `micro_project_files` directory
- Check that Flask-SQLAlchemy is installed: `pip install Flask-SQLAlchemy`
- Check for error messages in terminal

### Permission errors?
- Make sure you have write permissions in the directory
- On Windows, run as administrator if needed

### Database locked error?
- Close any other programs using the database
- Restart the Flask server

## ✅ Quick Start Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run init script: `python init_db.py`
- [ ] Verify `mess_service.db` file exists
- [ ] Start Flask server: `python app.py`
- [ ] Test login with sample credentials

## 🎯 Next Steps

After database is set up:
1. Start Flask server: `python app.py`
2. Open `index.html` in browser
3. Login and test all features!

---

**Remember:** SQLite creates the database file automatically - you just need to run `init_db.py` once!

