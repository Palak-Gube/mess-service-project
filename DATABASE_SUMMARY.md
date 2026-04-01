# Database Summary for Mess Service Project

## Overview
**Single Database Approach** - All tables in one database: `mess_service.db` (SQLite)

---

## 📋 **DATABASE TABLES SUMMARY**

### 🔐 **1. AUTHENTICATION & LOGIN/REGISTER**

#### **Table: `users`**
**Purpose:** Stores login credentials for both students and admins

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique user ID |
| `username` | String (80) | Unique username for login |
| `password` | String (255) | Hashed password |
| `role` | String (20) | 'student' or 'admin' |
| `created_at` | DateTime | Account creation timestamp |

**Used for:**
- ✅ User login (`/api/login`)
- ✅ User registration (`/api/register`)
- ✅ Role-based access control

---

### 👨‍🎓 **2. STUDENT DASHBOARD TABLES**

#### **Table: `students`**
**Purpose:** Student profile information

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key, FK → users.id) | Links to users table |
| `name` | String (100) | Student full name |
| `email` | String (100) | Unique email address |
| `phone` | String (20) | Contact number |
| `address` | Text | Student address |
| `student_id` | String (50) | Unique student ID |
| `enrollment_date` | Date | Date of enrollment |

**Used for:**
- ✅ Student profile display
- ✅ Profile updates
- ✅ User management (admin view)

---

#### **Table: `attendance`**
**Purpose:** Daily meal attendance tracking

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique attendance record ID |
| `student_id` | Integer (FK → students.id) | Which student |
| `date` | Date | Attendance date |
| `meal_type` | String (20) | 'breakfast', 'lunch', 'dinner' |
| `marked_by` | String (50) | 'self' or admin_id |
| `status` | String (20) | 'present' or 'absent' |
| `created_at` | DateTime | When marked |

**Unique Constraint:** One record per student per meal per day

**Used for:**
- ✅ Student marks own attendance (breakfast/lunch/dinner buttons)
- ✅ Admin marks attendance for students
- ✅ View attendance history
- ✅ Attendance reports

---

#### **Table: `subscriptions`**
**Purpose:** Student meal package subscriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique subscription ID |
| `student_id` | Integer (FK → students.id) | Which student |
| `package_id` | Integer (FK → packages.id) | Which package |
| `start_date` | Date | Subscription start |
| `end_date` | Date | Subscription end |
| `status` | String (20) | 'active', 'expired', 'cancelled' |
| `amount_paid` | Float | Payment amount |
| `created_at` | DateTime | Subscription creation |

**Used for:**
- ✅ Student selects meal package
- ✅ View subscription status
- ✅ Billing & payments
- ✅ Auto-expire expired subscriptions

---

#### **Table: `feedbacks`**
**Purpose:** Student feedback submissions

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique feedback ID |
| `student_id` | Integer (FK → students.id) | Which student |
| `feedback_text` | Text | Feedback content |
| `rating` | Integer | 1-5 stars rating |
| `menu_item_id` | Integer (FK → menu_items.id) | Optional menu item |
| `created_at` | DateTime | Feedback timestamp |

**Used for:**
- ✅ Student submits feedback
- ✅ Admin views all feedbacks
- ✅ Menu item ratings

---

#### **Table: `packages`**
**Purpose:** Available meal packages

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique package ID |
| `name` | String (100) | Package name |
| `price` | Float | Package price |
| `duration_days` | Integer | Duration in days |
| `features` | Text (JSON) | Package features |
| `description` | Text | Package description |

**Used for:**
- ✅ Display available packages
- ✅ Student selects package
- ✅ Subscription creation

---

### 👨‍💼 **3. ADMIN DASHBOARD TABLES**

#### **Table: `admins`**
**Purpose:** Admin profile information

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key, FK → users.id) | Links to users table |
| `name` | String (100) | Admin full name |
| `email` | String (100) | Unique email address |
| `phone` | String (20) | Contact number |
| `admin_id` | String (50) | Unique admin ID |
| `permissions` | Text (JSON) | Admin permissions |

**Used for:**
- ✅ Admin profile
- ✅ Permission management

---

#### **Table: `menu_items`**
**Purpose:** Daily menu items management

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (Primary Key) | Unique menu item ID |
| `name` | String (100) | Item name |
| `description` | Text | Item description |
| `category` | String (50) | 'Main Course', 'Beverage', etc. |
| `price` | Float | Item price |
| `date` | Date | Menu date |
| `image_path` | String (255) | Image file path |

**Used for:**
- ✅ Admin creates menu items (CRUD)
- ✅ Admin updates menu items
- ✅ Admin deletes menu items
- ✅ Display today's menu
- ✅ Menu management page

---

## 🔗 **TABLE RELATIONSHIPS**

```
users (1) ──→ (1) students
users (1) ──→ (1) admins
students (1) ──→ (many) attendance
students (1) ──→ (many) subscriptions
students (1) ──→ (many) feedbacks
packages (1) ──→ (many) subscriptions
menu_items (1) ──→ (many) feedbacks
```

---

## 📊 **DATA FLOW SUMMARY**

### **Student Dashboard Operations:**
1. **Login/Register** → `users` table
2. **Mark Attendance** → `attendance` table (CREATE)
3. **View Attendance** → `attendance` table (READ)
4. **Select Package** → `subscriptions` table (CREATE)
5. **View Bills** → `subscriptions` table (READ)
6. **Submit Feedback** → `feedbacks` table (CREATE)
7. **View Menu** → `menu_items` table (READ)

### **Admin Dashboard Operations:**
1. **Login/Register** → `users` table
2. **View All Students** → `students` table (READ)
3. **Mark Attendance** → `attendance` table (CREATE/UPDATE)
4. **View Attendance Report** → `attendance` table (READ)
5. **Menu Management** → `menu_items` table (CREATE/READ/UPDATE/DELETE)
6. **View Feedbacks** → `feedbacks` table (READ)
7. **View Subscriptions** → `subscriptions` table (READ/UPDATE)
8. **View Bills** → `subscriptions` table (READ)

---

## ✅ **CRUD OPERATIONS BY TABLE**

| Table | Create | Read | Update | Delete |
|-------|--------|------|--------|--------|
| `users` | ✅ Register | ✅ Login | ❌ | ❌ |
| `students` | ✅ Register | ✅ Profile/List | ✅ Profile | ❌ |
| `admins` | ✅ Register | ✅ Profile | ❌ | ❌ |
| `attendance` | ✅ Mark | ✅ View/Report | ✅ Admin edit | ✅ Admin delete |
| `menu_items` | ✅ Create | ✅ View | ✅ Update | ✅ Delete |
| `subscriptions` | ✅ Create | ✅ View | ✅ Status update | ❌ |
| `feedbacks` | ✅ Submit | ✅ View | ❌ | ❌ |
| `packages` | ✅ Create | ✅ View | ❌ | ❌ |

---

## 🎯 **KEY FEATURES BY DATABASE TABLE**

### **For Login/Register:**
- `users` - Authentication credentials

### **For Student Dashboard:**
- `students` - Profile data
- `attendance` - Mark/view attendance
- `subscriptions` - Package subscriptions
- `feedbacks` - Submit feedback
- `menu_items` - View menu
- `packages` - View packages

### **For Admin Dashboard:**
- `admins` - Admin profile
- `students` - View all students
- `attendance` - Mark/view/edit attendance
- `menu_items` - Full CRUD operations
- `subscriptions` - View/update subscriptions
- `feedbacks` - View all feedbacks
- `packages` - Manage packages

---

## 📝 **NOTES**

1. **Single Database:** All tables in `mess_service.db` (SQLite)
2. **Foreign Keys:** Proper relationships maintained 6
3. **Unique Constraints:** 
   - Username (unique)
   - Email (unique per role)
   - Attendance (one per student/meal/date)
4. **Cascade Deletes:** Deleting user deletes related student/admin records
5. **Auto-timestamps:** `created_at` fields auto-populated

---

## 🚀 **READY FOR 500 ROWS IMPORT**

All tables are ready to accept bulk data import. The structure supports:
- ✅ Importing 500 student records
- ✅ All CRUD operations
- ✅ Real-time updates visible in dashboards
- ✅ Database changes reflected in UI

