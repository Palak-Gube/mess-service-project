# 🚀 How to Start the Server

## ⚠️ **Important: You Must Be in the Correct Directory!**

The `app.py` file is located in the `micro_project_files` folder, not in the root directory.

---

## ✅ **Correct Way to Start Server:**

### **Option 1: Navigate First, Then Run**
```bash
cd micro_project_files
.\venv\Scripts\python.exe app.py
```

### **Option 2: Run from Root Directory**
```bash
.\venv\Scripts\python.exe micro_project_files\app.py
```

### **Option 3: Use the Batch File (Windows)**
```bash
cd micro_project_files
START_SERVER.bat
```

---

## 📁 **File Locations:**

- ✅ `app.py` is in: `micro_project_files/app.py`
- ✅ Database is in: `micro_project_files/instance/mess_service.db`
- ✅ Virtual environment: `micro_project_files/venv/`

---

## 🔍 **Check Current Directory:**

**Windows PowerShell:**
```powershell
pwd
# Should show: C:\Users\asus\OneDrive\Documents\GitHub\mess-service-microp\micro_project_files
```

**If you're in the wrong directory:**
```powershell
cd micro_project_files
```

---

## ✅ **Quick Start (Copy & Paste):**

```powershell
cd C:\Users\asus\OneDrive\Documents\GitHub\mess-service-microp\micro_project_files
.\venv\Scripts\python.exe app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

## 🛑 **To Stop Server:**

Press `Ctrl+C` in the terminal

---

## 🐛 **Common Errors:**

### **Error: "can't open file 'app.py'"**
**Solution:** You're in the wrong directory. Run:
```bash
cd micro_project_files
```

### **Error: "python.exe not found"**
**Solution:** Use the full path:
```bash
.\venv\Scripts\python.exe app.py
```

### **Error: "No module named 'flask'"**
**Solution:** Install requirements:
```bash
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 📝 **Step-by-Step:**

1. **Open Terminal/PowerShell**
2. **Navigate to project:**
   ```bash
   cd C:\Users\asus\OneDrive\Documents\GitHub\mess-service-microp\micro_project_files
   ```
3. **Start server:**
   ```bash
   .\venv\Scripts\python.exe app.py
   ```
4. **Open browser:**
   - Go to: `http://localhost:5000`
   - Or open: `index.html`

---

## ✅ **Verify It's Working:**

After starting the server, you should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Then open your browser and go to `http://localhost:5000`

---

**Remember: Always run commands from the `micro_project_files` directory!**

