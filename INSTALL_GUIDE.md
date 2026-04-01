# Installation Guide - Fixing Errors

## Error: "pip is not recognized"

This means Python/pip is not in your PATH. Try these solutions:

### Solution 1: Use `python -m pip` (Recommended)
Instead of `pip`, use:
```bash
python -m pip install -r requirements.txt
```

### Solution 2: Use `py -m pip` (Windows)
```bash
py -m pip install -r requirements.txt
```

### Solution 3: Check Python Installation
1. Check if Python is installed:
   ```bash
   python --version
   ```
   OR
   ```bash
   py --version
   ```

2. If Python is not installed:
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT:** Check "Add Python to PATH" during installation

## Step-by-Step Fix

### Step 1: Install Dependencies
Try these commands one by one until one works:

```bash
python -m pip install -r requirements.txt
```

OR

```bash
py -m pip install -r requirements.txt
```

OR

```bash
python3 -m pip install -r requirements.txt
```

### Step 2: Verify Installation
Check if Flask is installed:
```bash
python -m pip list | findstr Flask
```

### Step 3: Run Database Initialization
```bash
python init_db.py
```

## If Python is Not Installed

1. Download Python: https://www.python.org/downloads/
2. **CRITICAL:** During installation, check ✅ "Add Python to PATH"
3. Restart your terminal/PowerShell
4. Try again

## Alternative: Use Virtual Environment

If you have issues, create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python init_db.py
```


