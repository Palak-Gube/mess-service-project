# Database Structure for Mess Service

## Overview
You mentioned 3 databases. Here's a recommended structure:

## Option 1: Single Database with Multiple Tables (Recommended)
**Why?** Easier to manage, better relationships, single connection

### Database: `mess_service.db`

#### 1. **Authentication Table** (`users`)
Stores login credentials for both students and admins
```
- id (Primary Key)
- username (Unique)
- password (Hashed)
- role ('student' or 'admin')
- created_at
```

#### 2. **Students Table** (`students`)
Student details linked to users table
```
- id (Primary Key, Foreign Key -> users.id)
- name
- email
- phone
- address
- student_id (Unique)
- enrollment_date
```

#### 3. **Admins Table** (`admins`)
Admin details for large-scale service providers
```
- id (Primary Key, Foreign Key -> users.id)
- name
- email
- phone
- admin_id (Unique)
- permissions (JSON - what they can access)
```

#### 4. **Feedbacks Table** (`feedbacks`)
All student feedbacks
```
- id (Primary Key)
- student_id (Foreign Key -> students.id)
- feedback_text
- rating (1-5 stars)
- menu_item_id (optional)
- created_at
```

#### 5. **Meal Subscriptions Table** (`subscriptions`)
Student meal package subscriptions
```
- id (Primary Key)
- student_id (Foreign Key -> students.id)
- package_id (Foreign Key -> packages.id)
- start_date
- end_date
- status ('active', 'expired', 'cancelled')
- amount_paid
```

#### 6. **Packages Table** (`packages`)
Available meal packages
```
- id (Primary Key)
- name
- price
- duration_days
- features (JSON)
- description
```

#### 7. **Attendance Table** (`attendance`)
Daily meal attendance tracking
```
- id (Primary Key)
- student_id (Foreign Key -> students.id)
- date
- meal_type ('breakfast', 'lunch', 'dinner')
- marked_by (admin_id or 'self')
- status ('present', 'absent')
```

#### 8. **Menu Items Table** (`menu_items`)
Daily menu items
```
- id (Primary Key)
- name
- description
- category
- price
- date
```

---

## Option 2: Three Separate Databases (As You Mentioned)

### Database 1: `auth.db` (Login)
- `users` table (same as above)

### Database 2: `students.db` (Student Data)
- `students` table
- `feedbacks` table
- `subscriptions` table
- `attendance` table

### Database 3: `admin.db` (Admin Data)
- `admins` table
- `menu_items` table
- `packages` table

**Note:** This approach requires managing 3 database connections and is harder to maintain relationships.

---

## Recommendation
**Use Option 1 (Single Database)** because:
- ✅ Easier to maintain
- ✅ Better data relationships (foreign keys work properly)
- ✅ Single connection = better performance
- ✅ Simpler queries (can join tables easily)
- ✅ Standard practice for most applications

---

## How to Implement

### Using Flask-SQLAlchemy:
```python
# All tables in one database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_service.db'
db = SQLAlchemy(app)
```

### Using Separate Databases (if you prefer):
```python
# Multiple database connections
auth_db = SQLAlchemy()
students_db = SQLAlchemy()
admin_db = SQLAlchemy()
```

---

## Next Steps
1. Choose Option 1 or Option 2
2. I'll create the Flask models based on your choice
3. I'll create API endpoints for all operations


