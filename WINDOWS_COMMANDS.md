# Windows Commands - Quick Reference

## ⚠️ Important: Use `py` Instead of `python`

On your Windows system, use `py` command instead of `python`.

## ✅ Correct Commands for Windows

### Install Dependencies:
```bash
py -m pip install -r requirements.txt
```

### Initialize Database (One-time):
```bash
py init_db.py
```

### Start Flask Server:
```bash
py app.py
```

## ❌ Don't Use These (They Won't Work):
- ~~`python init_db.py`~~ → Use `py init_db.py`
- ~~`python app.py`~~ → Use `py app.py`
- ~~`pip install`~~ → Use `py -m pip install`

## 🚀 Quick Start Checklist

1. **Open PowerShell/Command Prompt**

2. **Navigate to project folder:**
   ```bash
   cd "C:\Users\asus\OneDrive\Documents\GitHub\mess-service-microp\micro_project_files"
   ```

3. **Install dependencies (if not done):**
   ```bash
   py -m pip install -r requirements.txt
   ```

4. **Initialize database (if not done):**
   ```bash
   py init_db.py
   ```

5. **Start Flask server:**
   ```bash
   py app.py
   ```

6. **Open browser:**
   - Go to: `http://localhost:5000` (backend)
   - Open `index.html` in browser (frontend)

## 📝 Why `py` Works But `python` Doesn't

- Windows Python Launcher (`py`) is installed and works
- `python` command is not in your PATH
- Both do the same thing, but use `py` on your system

## 🎯 Summary

**Always use:**
- `py` for Python commands
- `py -m pip` for pip commands

Your system is set up correctly - just use `py` instead of `python`!


