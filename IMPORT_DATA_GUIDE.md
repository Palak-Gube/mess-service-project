# 📥 How to Import Your 500-Row Database

## 🎯 Quick Start

### **Option 1: Import from CSV (Recommended)**

1. **Prepare your CSV file** with this format:
   ```csv
   name,email,phone,address,student_id,username,password,enrollment_date
   John Doe,john@example.com,1234567890,123 Main St,S001,john_doe,password123,2024-01-01
   Jane Smith,jane@example.com,0987654321,456 Oak Ave,S002,jane_smith,password123,2024-01-01
   ```

2. **Run the import script:**
   ```bash
   cd micro_project_files
   python import_data.py --csv your_file.csv
   ```

3. **Done!** Your 500 rows are now in the database.

---

## 📋 **Supported Formats**

### **1. CSV Format (Easiest)**

**Required Columns for Students:**
- `name` - Student full name
- `email` - Email address (must be unique)
- `phone` - Phone number (optional)
- `address` - Address (optional)
- `student_id` - Unique student ID (e.g., S001)
- `username` - Login username (must be unique)
- `password` - Login password (will be hashed)
- `enrollment_date` - Date in YYYY-MM-DD format

**Example CSV:**
```csv
name,email,phone,address,student_id,username,password,enrollment_date
John Doe,john@example.com,1234567890,123 Main St,S001,john_doe,pass123,2024-01-01
Jane Smith,jane@example.com,0987654321,456 Oak Ave,S002,jane_smith,pass123,2024-01-02
Bob Johnson,bob@example.com,1122334455,789 Pine Rd,S003,bob_johnson,pass123,2024-01-03
```

**Import Command:**
```bash
python import_data.py --csv students.csv
```

---

### **2. SQL Format**

**SQL File Format:**
```sql
-- Import students
INSERT INTO users (username, password, role) 
VALUES ('john_doe', 'hashed_password_here', 'student');

INSERT INTO students (id, name, email, phone, address, student_id, enrollment_date)
VALUES (1, 'John Doe', 'john@example.com', '1234567890', '123 Main St', 'S001', '2024-01-01');
```

**Note:** For SQL import, you need to:
1. Hash passwords manually OR
2. Use the CSV method (easier) OR
3. Let the import script handle it (recommended)

**Import Command:**
```bash
python import_data.py --sql data.sql
```

---

### **3. Excel Format**

**Excel File Requirements:**
- Sheet name: `Students` (or specify with `--sheet`)
- Same columns as CSV format
- First row should be headers

**Import Command:**
```bash
python import_data.py --excel students.xlsx
```

**Install Excel support (if needed):**
```bash
pip install openpyxl
```

---

## 🛠️ **Step-by-Step Import Process**

### **Step 1: Prepare Your Data**

**If you have data in another format:**
1. Export to CSV (easiest)
2. Make sure columns match the format above
3. Save as `students.csv` in `micro_project_files` folder

### **Step 2: Initialize Database (First Time Only)**

```bash
cd micro_project_files
python init_db.py
```

This creates the database structure.

### **Step 3: Import Your Data**

```bash
python import_data.py --csv students.csv
```

**Expected Output:**
```
✅ Database tables ready!
📥 Importing students from CSV: students.csv
  ✅ Imported 50 students...
  ✅ Imported 100 students...
  ✅ Imported 150 students...
  ...
  ✅ Imported 500 students...

✅ Import complete!
   Imported: 500 rows
   Skipped: 0 rows
```

### **Step 4: Verify Import**

```bash
python -c "from app import app, db, Student; app.app_context().push(); print(f'Total students: {Student.query.count()}')"
```

Or check in your admin dashboard after logging in.

---

## 📝 **Create Sample CSV File**

If you want to create a template CSV file:

```bash
python import_data.py --create-sample --rows 500
```

This creates `students_sample.csv` with 500 sample rows that you can edit.

---

## 🔧 **Advanced Options**

### **Import Different Tables**

**Menu Items:**
```bash
python import_data.py --csv menu_items.csv --table menu_items
```

**Packages:**
```bash
python import_data.py --csv packages.csv --table packages
```

### **CSV Format for Menu Items:**
```csv
name,description,category,price,date,image_path
Chicken Curry,Spicy chicken curry,Main Course,150.00,2024-01-15,
Vegetable Biryani,Rice with vegetables,Main Course,120.00,2024-01-15,
```

### **CSV Format for Packages:**
```csv
name,price,duration_days,features,description
Basic Daily,100,1,"[""Breakfast"", ""Lunch"", ""Dinner""]",Essential meals
Premium Weekly,600,7,"[""Breakfast"", ""Lunch"", ""Dinner"", ""Snacks""]",Full week plan
```

---

## ⚠️ **Important Notes**

### **Duplicate Prevention:**
- The script automatically skips rows with duplicate usernames
- The script automatically skips rows with duplicate emails
- Check the "Skipped" count in the output

### **Password Handling:**
- Passwords are automatically hashed (secure)
- Original passwords in CSV are not stored
- Students can login with the password from your CSV

### **Date Format:**
- Use `YYYY-MM-DD` format (e.g., `2024-01-15`)
- If date is missing, defaults to today's date

### **Required Fields:**
- **Students:** name, email, student_id (or auto-generated)
- **Optional:** phone, address, enrollment_date

---

## 🐛 **Troubleshooting**

### **Error: "File not found"**
- Make sure CSV file is in `micro_project_files` folder
- Check file name spelling
- Use full path if needed: `--csv C:/path/to/file.csv`

### **Error: "Username already exists"**
- The script skips duplicate usernames automatically
- Check your CSV for duplicates
- Or delete existing data first

### **Error: "Email already exists"**
- The script skips duplicate emails automatically
- Each student must have unique email

### **Import is slow:**
- Normal for 500 rows (takes 10-30 seconds)
- Progress is shown every 50 rows
- Be patient, it's working!

### **Some rows skipped:**
- Check the error messages in output
- Common issues:
  - Missing required fields
  - Invalid date format
  - Duplicate username/email

---

## 📊 **Verify Your Import**

### **Method 1: Check Database Directly**
```bash
python -c "from app import app, db, Student; app.app_context().push(); print(f'Students: {Student.query.count()}')"
```

### **Method 2: Use Admin Dashboard**
1. Start Flask: `python app.py`
2. Login as admin (username: `admin`, password: `admin123`)
3. Go to "User Management" page
4. You should see all imported students

### **Method 3: Check via API**
```bash
# Start Flask server first
curl http://localhost:5000/api/admin/students
```

---

## 🎯 **Complete Example**

**1. Create sample CSV:**
```bash
python import_data.py --create-sample --rows 500
```

**2. Edit the CSV file** (`students_sample.csv`) with your real data

**3. Import:**
```bash
python import_data.py --csv students_sample.csv
```

**4. Start Flask and test:**
```bash
python app.py
```

**5. Login and verify:**
- Admin dashboard → User Management → See all 500 students
- Try logging in with one of the imported usernames

---

## ✅ **Success Checklist**

After import, verify:
- [ ] Total students count matches (500)
- [ ] Can login with imported usernames
- [ ] Students appear in admin dashboard
- [ ] No duplicate errors
- [ ] All data fields are correct

---

## 🚀 **Quick Commands Reference**

```bash
# Create sample CSV (500 rows)
python import_data.py --create-sample --rows 500

# Import from CSV
python import_data.py --csv students.csv

# Import from SQL
python import_data.py --sql data.sql

# Import from Excel
python import_data.py --excel students.xlsx

# Import menu items
python import_data.py --csv menu.csv --table menu_items

# Import packages
python import_data.py --csv packages.csv --table packages
```

---

## 💡 **Tips**

1. **Backup first:** Copy `mess_service.db` before importing
2. **Test with small file:** Try 10 rows first, then full 500
3. **Check format:** Make sure CSV has correct headers
4. **Use sample:** Generate sample CSV first to see format
5. **Verify after:** Always check admin dashboard after import

---

**Your 500 rows will be imported and ready to use! 🎉**

