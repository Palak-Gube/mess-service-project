# ⚡ Quick Import Guide - 3 Steps

## 🎯 Import Your 500 Rows in 3 Steps

### **Step 1: Prepare Your CSV File**

Your CSV file should have these columns:
```
name,email,phone,address,student_id,username,password,enrollment_date
```

**Example:**
```csv
name,email,phone,address,student_id,username,password,enrollment_date
John Doe,john@example.com,1234567890,123 Main St,S001,john_doe,pass123,2024-01-01
Jane Smith,jane@example.com,0987654321,456 Oak Ave,S002,jane_smith,pass123,2024-01-01
```

**OR** create a sample file first:
```bash
python import_data.py --create-sample --rows 500
```
This creates `students_sample.csv` - edit it with your data!

---

### **Step 2: Run Import Script**

```bash
cd micro_project_files
python import_data.py --csv your_file.csv
```

**Replace `your_file.csv` with your actual file name!**

---

### **Step 3: Verify Import**

Start Flask and check:
```bash
python app.py
```

Then:
1. Open admin dashboard
2. Login (username: `admin`, password: `admin123`)
3. Go to "User Management"
4. You should see all 500 students!

---

## 📋 **What You Need**

1. ✅ CSV file with your 500 rows
2. ✅ File saved in `micro_project_files` folder
3. ✅ Correct column headers (see Step 1)

---

## 🚨 **Common Issues**

**"File not found"**
- Make sure file is in `micro_project_files` folder
- Check file name spelling

**"Username already exists"**
- Script skips duplicates automatically
- Check your CSV for duplicate usernames

**"Import is slow"**
- Normal! 500 rows takes 10-30 seconds
- Progress shown every 50 rows

---

## ✅ **Success!**

After import:
- ✅ All 500 students in database
- ✅ Can login with any username from CSV
- ✅ Students visible in admin dashboard
- ✅ All features work with your data

---

## 📞 **Need Help?**

See full guide: `IMPORT_DATA_GUIDE.md`

