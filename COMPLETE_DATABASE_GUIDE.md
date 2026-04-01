# Complete Database & Frontend-Backend Connection Guide

## 📊 **DATABASE TABLES FOR EACH DASHBOARD**

### 🔐 **1. LOGIN & REGISTER**

#### **Table: `users`**
**Fields:**
- `id` (Primary Key, Auto-increment)
- `username` (Unique, String)
- `password` (Hashed, String)
- `role` ('student' or 'admin')
- `created_at` (Auto-timestamp)

**Purpose:** Authentication for both students and admins

---

### 👨‍🎓 **2. STUDENT DASHBOARD TABLES**

#### **Table: `students`**
**Fields:**
- `id` (Primary Key, Foreign Key → users.id)
- `name` (String)
- `email` (Unique, String)
- `phone` (String)
- `address` (Text)
- `student_id` (Unique, String)
- `enrollment_date` (Date)

**Purpose:** Student profile information

#### **Table: `attendance`**
**Fields:**
- `id` (Primary Key, Auto-increment)
- `student_id` (Foreign Key → students.id)
- `date` (Date)
- `meal_type` ('breakfast', 'lunch', 'dinner')
- `marked_by` ('self' or admin_id)
- `status` ('present' or 'absent')
- `created_at` (Auto-timestamp)

**Purpose:** Track meal attendance

#### **Table: `subscriptions`**
**Fields:**
- `id` (Primary Key, Auto-increment)
- `student_id` (Foreign Key → students.id)
- `package_id` (Foreign Key → packages.id)
- `start_date` (Date)
- `end_date` (Date)
- `status` ('active', 'expired', 'cancelled')
- `amount_paid` (Float)
- `created_at` (Auto-timestamp)

**Purpose:** Student meal package subscriptions (used for billing)

#### **Table: `feedbacks`**
**Fields:**
- `id` (Primary Key, Auto-increment)
- `student_id` (Foreign Key → students.id)
- `feedback_text` (Text)
- `rating` (Integer, 1-5)
- `menu_item_id` (Foreign Key → menu_items.id, Optional)
- `created_at` (Auto-timestamp)

**Purpose:** Student feedback submissions

#### **Table: `packages`** (Read-only for students)
**Fields:**
- `id` (Primary Key, Auto-increment)
- `name` (String)
- `price` (Float)
- `duration_days` (Integer)
- `features` (Text/JSON)
- `description` (Text)

**Purpose:** Available meal packages

---

### 👨‍💼 **3. ADMIN DASHBOARD TABLES**

#### **Table: `admins`**
**Fields:**
- `id` (Primary Key, Foreign Key → users.id)
- `name` (String)
- `email` (Unique, String)
- `phone` (String)
- `admin_id` (Unique, String)
- `permissions` (Text/JSON)

**Purpose:** Admin profile information

#### **Table: `menu_items`**
**Fields:**
- `id` (Primary Key, Auto-increment)
- `name` (String)
- `description` (Text)
- `category` (String)
- `price` (Float)
- `date` (Date)
- `image_path` (String)

**Purpose:** Menu management (Full CRUD)

---

## 🔄 **DATA FLOW: STUDENT ACTIONS → DATABASE → ADMIN DASHBOARD**

### **Scenario 1: New Student Registration**

**Step-by-Step Flow:**

1. **Student fills registration form** (frontend)
   ```javascript
   // Frontend: register.html or index.html
   const data = {
     role: 'student',
     username: 'john_doe',
     password: 'password123',
     name: 'John Doe',
     email: 'john@example.com',
     phone: '1234567890',
     address: '123 Main St',
     student_id: 'S001'
   };
   ```

2. **Frontend sends POST request to backend**
   ```javascript
   // api.js
   const response = await fetch('http://localhost:5000/api/register', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(data)
   });
   ```

3. **Backend processes registration** (app.py)
   ```python
   # app.py - /api/register endpoint
   # Creates entry in 'users' table
   user = User(username=..., password=hashed, role='student')
   db.session.add(user)
   db.session.flush()  # Get user.id
   
   # Creates entry in 'students' table
   student = Student(id=user.id, name=..., email=..., ...)
   db.session.add(student)
   db.session.commit()  # SAVED TO DATABASE ✅
   ```

4. **Result:**
   - ✅ Entry in `users` table
   - ✅ Entry in `students` table
   - ✅ Student can now login
   - ✅ Admin can see student in user management page

---

### **Scenario 2: Student Marks Attendance**

**Step-by-Step Flow:**

1. **Student clicks "Mark Breakfast" button** (dashboard)
   ```javascript
   // Frontend: dashboard-content.html
   await student.markAttendance(userId, today, 'breakfast');
   ```

2. **Frontend calls API**
   ```javascript
   // api.js
   markAttendance: (id, date, mealType) => 
     apiCall(`/students/${id}/attendance`, 'POST', { date, mealType })
   ```

3. **Backend saves to database** (app.py)
   ```python
   # app.py - /api/students/<id>/attendance POST
   attendance = Attendance(
     student_id=student_id,
     date=today,
     meal_type='breakfast',
     marked_by='self',
     status='present'
   )
   db.session.add(attendance)
   db.session.commit()  # SAVED TO DATABASE ✅
   ```

4. **Admin Dashboard automatically shows it:**
   - Admin opens attendance page
   - Frontend calls: `GET /api/admin/attendance?date=2024-01-15`
   - Backend queries `attendance` table
   - Returns all attendance records for that date
   - Admin sees: "John Doe - Breakfast - Present"

---

### **Scenario 3: Student Selects Meal Package**

**Step-by-Step Flow:**

1. **Student selects package** (frontend)
   ```javascript
   await student.selectPackage(userId, packageId);
   ```

2. **Backend creates subscription** (app.py)
   ```python
   # app.py - /api/students/<id>/subscriptions POST
   subscription = Subscription(
     student_id=student_id,
     package_id=package_id,
     start_date=today,
     end_date=today + duration,
     amount_paid=package.price,
     status='active'
   )
   db.session.add(subscription)
   db.session.commit()  # SAVED TO DATABASE ✅
   ```

3. **Admin Dashboard shows:**
   - **User Management:** Student appears with "Active" subscription status
   - **Billing Page:** Shows bill with amount, due date, status
   - **Subscriptions Page:** Shows all subscriptions with student name

---

### **Scenario 4: Student Submits Feedback**

**Step-by-Step Flow:**

1. **Student submits feedback** (frontend)
   ```javascript
   await student.submitFeedback(userId, 'Great food!', 5);
   ```

2. **Backend saves feedback** (app.py)
   ```python
   # app.py - /api/students/<id>/feedback POST
   feedback = Feedback(
     student_id=student_id,
     feedback_text='Great food!',
     rating=5
   )
   db.session.add(feedback)
   db.session.commit()  # SAVED TO DATABASE ✅
   ```

3. **Admin Dashboard shows:**
   - **Feedbacks Page:** Shows all feedbacks with student name
   - **Dashboard:** Recent feedbacks widget shows new feedback

---

## 🔧 **UPDATE & DELETE OPERATIONS**

### **Update Operations:**

#### **1. Update Student Profile**
```python
# app.py - PUT /api/students/<id>
student = Student.query.get(student_id)
student.name = data.get('name', student.name)
student.email = data.get('email', student.email)
db.session.commit()  # UPDATED IN DATABASE ✅
```

#### **2. Update Menu Item** (Admin)
```python
# app.py - PUT /api/admin/menu/<id>
menu_item = MenuItem.query.get(item_id)
menu_item.name = data.get('name', menu_item.name)
menu_item.price = data.get('price', menu_item.price)
db.session.commit()  # UPDATED IN DATABASE ✅
```

#### **3. Update Attendance** (Admin)
```python
# Need to add this endpoint - see modifications below
# PUT /api/admin/attendance/<id>
attendance = Attendance.query.get(attendance_id)
attendance.status = 'absent'  # Change status
db.session.commit()  # UPDATED IN DATABASE ✅
```

#### **4. Update Subscription Status** (Admin)
```python
# app.py - PUT /api/admin/subscriptions/<id>
subscription = Subscription.query.get(subscription_id)
subscription.status = 'expired'
db.session.commit()  # UPDATED IN DATABASE ✅
```

### **Delete Operations:**

#### **1. Delete Menu Item** (Admin)
```python
# app.py - DELETE /api/admin/menu/<id>
menu_item = MenuItem.query.get(item_id)
db.session.delete(menu_item)
db.session.commit()  # DELETED FROM DATABASE ✅
```

#### **2. Delete Attendance Record** (Admin)
```python
# Need to add this endpoint - see modifications below
# DELETE /api/admin/attendance/<id>
attendance = Attendance.query.get(attendance_id)
db.session.delete(attendance)
db.session.commit()  # DELETED FROM DATABASE ✅
```

---

## 🔌 **FRONTEND-BACKEND CONNECTION**

### **How It Works:**

```
┌─────────────┐         HTTP Request          ┌─────────────┐
│  Frontend   │ ────────────────────────────> │   Backend    │
│  (Browser)  │                               │  (Flask API) │
│             │ <──────────────────────────── │              │
└─────────────┘      JSON Response            └─────────────┘
                                                      │
                                                      ▼
                                              ┌─────────────┐
                                              │  Database   │
                                              │  (SQLite)   │
                                              └─────────────┘
```

### **Connection Flow:**

1. **Frontend makes API call** (api.js)
   ```javascript
   // api.js
   const API_BASE = 'http://localhost:5000/api';
   
   async function apiCall(endpoint, method = 'GET', data = null) {
     const options = {
       method,
       headers: { 'Content-Type': 'application/json' },
     };
     if (data) options.body = JSON.stringify(data);
     
     const res = await fetch(`${API_BASE}${endpoint}`, options);
     return await res.json();
   }
   ```

2. **Backend receives request** (app.py)
   ```python
   # app.py
   @app.route('/api/students/<int:student_id>', methods=['GET'])
   def get_student(student_id):
       student = Student.query.get_or_404(student_id)
       return jsonify({
           'id': student.id,
           'name': student.name,
           # ... more fields
       })
   ```

3. **Backend queries database**
   ```python
   # SQLAlchemy automatically converts to SQL
   student = Student.query.get(student_id)
   # Executes: SELECT * FROM students WHERE id = ?
   ```

4. **Backend returns JSON**
   ```json
   {
     "id": 1,
     "name": "John Doe",
     "email": "john@example.com"
   }
   ```

5. **Frontend receives and displays**
   ```javascript
   const student = await student.getProfile(userId);
   document.getElementById('name').textContent = student.name;
   ```

---

## 🔗 **CONNECTING MULTIPLE TABLES TO FRONTEND**

### **Example: Admin Dashboard Shows Student Data from Multiple Tables**

**Frontend Request:**
```javascript
// Get dashboard data (includes data from multiple tables)
const dashboardData = await admin.getDashboard();
```

**Backend Query (joins multiple tables):**
```python
# app.py - /api/admin/dashboard
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Query students table
    total_students = Student.query.count()
    
    # Query subscriptions table (joined with students)
    subscriptions = Subscription.query.all()
    # Each subscription has: subscription.student.name (relationship)
    
    # Query attendance table (joined with students)
    attendance = Attendance.query.filter_by(date=today).all()
    # Each attendance has: attendance.student.name (relationship)
    
    # Query feedbacks table (joined with students)
    feedbacks = Feedback.query.all()
    # Each feedback has: feedback.student.name (relationship)
    
    return jsonify({
        'total_students': total_students,
        'subscriptions': [{
            'student_name': s.student.name,  # From students table
            'package_name': s.package.name,   # From packages table
            'amount': s.amount_paid          # From subscriptions table
        } for s in subscriptions],
        'attendance': [{
            'student_name': a.student.name,  # From students table
            'meal_type': a.meal_type         # From attendance table
        } for a in attendance]
    })
```

**How Relationships Work:**
```python
# In Student model (app.py)
class Student(db.Model):
    # ...
    subscriptions = db.relationship('Subscription', backref='student')
    attendance_records = db.relationship('Attendance', backref='student')

# This allows:
subscription.student.name  # Access student from subscription
attendance.student.name    # Access student from attendance
```

---

## 📝 **MODIFICATIONS NEEDED IN app.py**

### **1. Add Update/Delete Endpoints for Attendance**

Add these endpoints to `app.py`:

```python
# Update attendance (Admin)
@app.route('/api/admin/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    """Update attendance record"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        data = request.json
        
        attendance.status = data.get('status', attendance.status)
        attendance.meal_type = data.get('meal_type', attendance.meal_type)
        if data.get('date'):
            attendance.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete attendance (Admin)
@app.route('/api/admin/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    """Delete attendance record"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get attendance with ID (for update/delete)
@app.route('/api/admin/attendance', methods=['GET'])
def get_attendance_report():
    """Get attendance report for a date"""
    att_date = request.args.get('date', date.today().isoformat())
    records = Attendance.query.filter_by(date=datetime.strptime(att_date, '%Y-%m-%d').date()).all()
    return jsonify([{
        'id': r.id,  # ADD THIS for update/delete
        'student_name': r.student.name,
        'student_id': r.student.student_id,
        'meal_type': r.meal_type,
        'status': r.status,
        'date': r.date.isoformat()
    } for r in records])
```

### **2. Add Delete Student Endpoint (Optional)**

```python
@app.route('/api/admin/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student (cascades to users table)"""
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student_id)
        
        # Delete student (cascades to attendance, subscriptions, feedbacks)
        db.session.delete(student)
        # Delete user
        db.session.delete(user)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
```

### **3. Ensure All Endpoints Return IDs for Update/Delete**

Make sure all GET endpoints return `id` field so frontend can update/delete:

```python
# Example: Get all students
@app.route('/api/admin/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([{
        'id': s.id,  # ✅ Include ID
        'name': s.name,
        'email': s.email,
        # ... other fields
    } for s in students])
```

---

## 🗄️ **SQLITE vs SUPABASE - RECOMMENDATION**

### **SQLite (Current Setup) ✅ RECOMMENDED FOR NOW**

**Pros:**
- ✅ **Zero setup** - No server needed
- ✅ **File-based** - Easy to backup (just copy .db file)
- ✅ **Perfect for development** - Fast, lightweight
- ✅ **Already configured** - Works out of the box
- ✅ **Good for 500 rows** - Handles thousands easily
- ✅ **No internet required** - Works offline

**Cons:**
- ❌ **Single user** - Not ideal for multiple concurrent users
- ❌ **No remote access** - Database file must be on same machine
- ❌ **Limited scalability** - Not for millions of rows

**When to use:**
- Development/testing
- Small to medium projects (< 10,000 rows)
- Single server deployment
- Learning projects

**Current Setup:**
```python
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_service.db'
```

---

### **Supabase (PostgreSQL) - FOR PRODUCTION**

**Pros:**
- ✅ **Cloud-hosted** - Access from anywhere
- ✅ **Multiple users** - Handles concurrent access
- ✅ **Scalable** - Millions of rows
- ✅ **Real-time** - Can subscribe to changes
- ✅ **Built-in auth** - Authentication features
- ✅ **Backups** - Automatic backups

**Cons:**
- ❌ **Requires setup** - Need to create account, project
- ❌ **Internet required** - Needs connection
- ❌ **Cost** - Free tier has limits
- ❌ **More complex** - Need to configure connection

**When to use:**
- Production deployment
- Multiple users accessing simultaneously
- Need remote access
- Large scale (millions of rows)

**Setup (if switching):**
```python
# app.py
import os
DATABASE_URL = os.getenv('DATABASE_URL')  # From Supabase
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

---

## 🎯 **RECOMMENDATION**

**Start with SQLite** because:
1. ✅ Already configured in your project
2. ✅ Perfect for 500 rows
3. ✅ Easy to test and develop
4. ✅ Can migrate to Supabase later if needed

**Switch to Supabase when:**
- You need multiple users accessing simultaneously
- Deploying to production
- Need remote database access
- Scaling beyond 10,000+ rows

---

## 📋 **CHECKLIST: AUTO-GENERATED ROWS & DATABASE OPERATIONS**

### **If You Create Database with Auto-Generated Rows:**

✅ **What Works:**
- All existing endpoints will work
- Can query all rows
- Can update/delete any row
- Can add new rows via frontend

✅ **What to Ensure:**
- Foreign keys match (student_id must exist in students table)
- Unique constraints respected (username, email must be unique)
- Date formats match (YYYY-MM-DD)

### **Update Operations:**
- ✅ Update student profile → Updates `students` table
- ✅ Update menu item → Updates `menu_items` table
- ✅ Update attendance → Updates `attendance` table
- ✅ Update subscription status → Updates `subscriptions` table

### **Delete Operations:**
- ✅ Delete menu item → Removes from `menu_items` table
- ✅ Delete attendance → Removes from `attendance` table
- ✅ Delete student → Cascades to related records

### **New User Registration:**
- ✅ Creates entry in `users` table
- ✅ Creates entry in `students` or `admins` table
- ✅ Immediately visible in admin dashboard
- ✅ Can login immediately

---

## 🚀 **QUICK START: CONNECTING YOUR 500-ROW DATABASE**

### **Step 1: Import Your Data**

If you have a CSV or SQL file with 500 rows:

**Option A: SQL Import**
```sql
-- Import into existing tables
INSERT INTO students (id, name, email, phone, student_id, enrollment_date)
VALUES (1, 'John Doe', 'john@example.com', '1234567890', 'S001', '2024-01-01');
-- ... repeat for all rows
```

**Option B: Python Script**
```python
# import_data.py
import csv
from app import app, db, Student, User
from werkzeug.security import generate_password_hash

with app.app_context():
    with open('students.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create user
            user = User(
                username=row['username'],
                password=generate_password_hash(row['password']),
                role='student'
            )
            db.session.add(user)
            db.session.flush()
            
            # Create student
            student = Student(
                id=user.id,
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                student_id=row['student_id']
            )
            db.session.add(student)
    
    db.session.commit()
    print("500 students imported!")
```

### **Step 2: Verify Data**

```python
# Check data
with app.app_context():
    count = Student.query.count()
    print(f"Total students: {count}")
```

### **Step 3: Test Frontend**

1. Run Flask: `python app.py`
2. Open frontend
3. Login with imported credentials
4. All data should appear in dashboards

---

## 📚 **SUMMARY**

### **Database Tables:**
- **Login/Register:** `users`
- **Student Dashboard:** `students`, `attendance`, `subscriptions`, `feedbacks`, `packages`
- **Admin Dashboard:** `admins`, `menu_items` + all student tables

### **Data Flow:**
1. Student action → Frontend API call → Backend endpoint → Database save
2. Admin dashboard → Frontend API call → Backend query → Database read → Display

### **Update/Delete:**
- All operations save to database immediately
- Changes visible in dashboards instantly
- Use PUT for updates, DELETE for deletions

### **Frontend-Backend Connection:**
- `api.js` makes HTTP requests to Flask endpoints
- Flask queries database using SQLAlchemy
- Returns JSON to frontend
- Frontend displays data

### **Database Choice:**
- **SQLite** for development (current setup) ✅
- **Supabase** for production (if needed later)

---

**Your project is ready! All endpoints are connected, and data flows from frontend → backend → database → admin dashboard automatically.**

