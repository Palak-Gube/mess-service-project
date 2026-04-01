"""
Supabase Database Setup Script
Creates all tables and populates with 100+ sample records
"""
import sys
import io
import os
from datetime import datetime, date, timedelta
import random
from werkzeug.security import generate_password_hash

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Try to import Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase client not installed. Install with: pip install supabase")

from app import app, db, User, Student, Admin, Package, Subscription, Attendance, Feedback, MenuItem

def setup_supabase_connection():
    """Setup Supabase connection from environment variables"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables not set!")
        print("\n📝 Setup Instructions:")
        print("1. Go to https://supabase.com and create a project")
        print("2. Go to Project Settings > API")
        print("3. Copy 'Project URL' and 'anon/public key'")
        print("4. Set environment variables:")
        print("   Windows PowerShell:")
        print("   $env:SUPABASE_URL='your-project-url'")
        print("   $env:SUPABASE_KEY='your-anon-key'")
        print("\n   Or create a .env file:")
        print("   SUPABASE_URL=your-project-url")
        print("   SUPABASE_KEY=your-anon-key")
        return None
    
    if SUPABASE_AVAILABLE:
        try:
            supabase: Client = create_client(supabase_url, supabase_key)
            print("✅ Connected to Supabase!")
            return supabase
        except Exception as e:
            print(f"❌ Error connecting to Supabase: {str(e)}")
            return None
    else:
        print("❌ Supabase client not available")
        return None

def create_tables_sql():
    """Generate SQL to create all tables in Supabase"""
    sql = """
-- ============================================
-- MESS SERVICE DATABASE SCHEMA FOR SUPABASE
-- ============================================

-- 1. Users table (Authentication)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE
);

-- 3. Admins table
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    admin_id VARCHAR(50) UNIQUE NOT NULL,
    permissions TEXT
);

-- 4. Packages table
CREATE TABLE IF NOT EXISTS packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    duration_days INTEGER NOT NULL,
    features TEXT,
    description TEXT
);

-- 5. Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled')),
    amount_paid DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    meal_type VARCHAR(20) NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner')),
    marked_by VARCHAR(50),
    status VARCHAR(20) DEFAULT 'present' CHECK (status IN ('present', 'absent')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, date, meal_type)
);

-- 7. Feedbacks table
CREATE TABLE IF NOT EXISTS feedbacks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    feedback_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    menu_item_id INTEGER REFERENCES menu_items(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    date DATE DEFAULT CURRENT_DATE,
    image_path VARCHAR(255)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_student_id ON students(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student_date ON attendance(student_id, date);
CREATE INDEX IF NOT EXISTS idx_subscriptions_student ON subscriptions(student_id);
CREATE INDEX IF NOT EXISTS idx_feedbacks_student ON feedbacks(student_id);

"""
    return sql

def generate_sample_data():
    """Generate 100+ sample records"""
    print("\n📝 Generating sample data...")
    
    sample_data = {
        'users': [],
        'students': [],
        'packages': [],
        'subscriptions': [],
        'attendance': [],
        'feedbacks': [],
        'menu_items': []
    }
    
    # Sample names
    first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry',
                   'Ivy', 'Jack', 'Kate', 'Leo', 'Mia', 'Noah', 'Olivia', 'Paul', 'Quinn', 'Rachel',
                   'Sam', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier', 'Yara', 'Zoe']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee']
    
    # Generate 100 students
    for i in range(1, 101):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        username = f"{first_name.lower()}{i}"
        student_id = f"S{i:04d}"
        
        # Create user
        user = {
            'username': username,
            'password': generate_password_hash('password123'),
            'role': 'student'
        }
        sample_data['users'].append(user)
        
        # Create student (will link after user is created)
        student = {
            'name': name,
            'email': email,
            'phone': f"{random.randint(1000000000, 9999999999)}",
            'address': f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Maple'])} Street",
            'student_id': student_id,
            'enrollment_date': (date.today() - timedelta(days=random.randint(1, 365))).isoformat()
        }
        sample_data['students'].append(student)
    
    # Generate packages
    packages_data = [
        {'name': 'Basic Daily', 'price': 100.00, 'duration_days': 1, 'features': '["Breakfast", "Lunch", "Dinner"]', 'description': 'Essential meals for a day'},
        {'name': 'Premium Weekly', 'price': 600.00, 'duration_days': 7, 'features': '["Breakfast", "Lunch", "Dinner", "Snacks"]', 'description': 'Full week with extras'},
        {'name': 'VIP Monthly', 'price': 2500.00, 'duration_days': 30, 'features': '["All meals", "Beverages", "Priority seating"]', 'description': 'Complete monthly plan'},
        {'name': 'Economy Weekly', 'price': 500.00, 'duration_days': 7, 'features': '["Breakfast", "Lunch", "Dinner"]', 'description': 'Budget-friendly weekly plan'},
        {'name': 'Deluxe Monthly', 'price': 3000.00, 'duration_days': 30, 'features': '["All meals", "Premium beverages", "VIP seating", "Special events"]', 'description': 'Premium monthly experience'}
    ]
    sample_data['packages'] = packages_data
    
    # Generate subscriptions (50% of students have subscriptions)
    for i in range(1, 51):
        student_id = i
        package_id = random.randint(1, len(packages_data))
        package = packages_data[package_id - 1]
        start_date = (date.today() - timedelta(days=random.randint(1, 30))).isoformat()
        end_date = (datetime.strptime(start_date, '%Y-%m-%d').date() + timedelta(days=package['duration_days'])).isoformat()
        status = 'active' if datetime.strptime(end_date, '%Y-%m-%d').date() >= date.today() else 'expired'
        
        subscription = {
            'student_id': student_id,
            'package_id': package_id,
            'start_date': start_date,
            'end_date': end_date,
            'status': status,
            'amount_paid': package['price']
        }
        sample_data['subscriptions'].append(subscription)
    
    # Generate attendance (last 30 days for 80% of students)
    meal_types = ['breakfast', 'lunch', 'dinner']
    for i in range(1, 81):  # 80 students
        student_id = i
        for day_offset in range(30):  # Last 30 days
            date_str = (date.today() - timedelta(days=day_offset)).isoformat()
            # Randomly mark some meals
            for meal_type in meal_types:
                if random.random() > 0.3:  # 70% chance of marking attendance
                    attendance = {
                        'student_id': student_id,
                        'date': date_str,
                        'meal_type': meal_type,
                        'marked_by': 'self',
                        'status': 'present'
                    }
                    sample_data['attendance'].append(attendance)
    
    # Generate feedbacks (60 students gave feedback)
    feedback_texts = [
        'Great food quality!',
        'Excellent service',
        'Could improve variety',
        'Very satisfied',
        'Good value for money',
        'Needs more vegetarian options',
        'Amazing experience',
        'Food was cold',
        'Best mess service ever!',
        'Needs improvement in timing'
    ]
    for i in range(1, 61):
        student_id = i
        feedback = {
            'student_id': student_id,
            'feedback_text': random.choice(feedback_texts),
            'rating': random.randint(3, 5),
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
        }
        sample_data['feedbacks'].append(feedback)
    
    # Generate menu items
    menu_items_data = [
        {'name': 'Chicken Curry', 'description': 'Spicy chicken curry', 'category': 'Main Course', 'price': 150.00},
        {'name': 'Vegetable Biryani', 'description': 'Rice with vegetables', 'category': 'Main Course', 'price': 120.00},
        {'name': 'Dal Fry', 'description': 'Lentil curry', 'category': 'Main Course', 'price': 80.00},
        {'name': 'Paneer Tikka', 'description': 'Grilled cottage cheese', 'category': 'Main Course', 'price': 140.00},
        {'name': 'Rice', 'description': 'Steamed basmati rice', 'category': 'Main Course', 'price': 50.00},
        {'name': 'Roti', 'description': 'Indian bread', 'category': 'Main Course', 'price': 20.00},
        {'name': 'Salad', 'description': 'Fresh vegetable salad', 'category': 'Side Dish', 'price': 40.00},
        {'name': 'Soup', 'description': 'Hot soup of the day', 'category': 'Starter', 'price': 60.00},
        {'name': 'Ice Cream', 'description': 'Vanilla ice cream', 'category': 'Dessert', 'price': 50.00},
        {'name': 'Tea', 'description': 'Hot tea', 'category': 'Beverage', 'price': 15.00}
    ]
    sample_data['menu_items'] = menu_items_data
    
    print(f"✅ Generated:")
    print(f"   - {len(sample_data['users'])} users")
    print(f"   - {len(sample_data['students'])} students")
    print(f"   - {len(sample_data['packages'])} packages")
    print(f"   - {len(sample_data['subscriptions'])} subscriptions")
    print(f"   - {len(sample_data['attendance'])} attendance records")
    print(f"   - {len(sample_data['feedbacks'])} feedbacks")
    print(f"   - {len(sample_data['menu_items'])} menu items")
    
    return sample_data

def setup_supabase_database():
    """Setup Supabase database with tables and sample data"""
    print("🚀 Setting up Supabase Database...")
    print("=" * 50)
    
    # Check if using Supabase or SQLite
    use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
    
    if use_supabase and SUPABASE_AVAILABLE:
        supabase = setup_supabase_connection()
        if not supabase:
            print("\n⚠️  Falling back to SQLite...")
            use_supabase = False
    
    # Always use SQLite for now (Supabase setup requires manual SQL execution)
    # To use Supabase, set USE_SUPABASE=true and run SQL manually in Supabase dashboard
    use_supabase = False  # Force SQLite for automatic setup
    
    if not use_supabase:
        # Use SQLite (local database)
        print("\n📦 Using SQLite Database (Local)")
        print("=" * 50)
        print("💡 To use Supabase, see SUPABASE_SETUP_GUIDE.md")
        print("=" * 50)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created!")
            
            # Check if data already exists
            existing_students = Student.query.count()
            if existing_students > 0:
                print(f"⚠️  Database already has {existing_students} students.")
                print("   Adding 100+ more sample records...")
                # Continue to add more data
            
            # Generate sample data
            sample_data = generate_sample_data()
            
            # Insert users and students
            print("\n📥 Inserting users and students...")
            for i, (user_data, student_data) in enumerate(zip(sample_data['users'], sample_data['students']), 1):
                try:
                    # Create user
                    user = User(
                        username=user_data['username'],
                        password=user_data['password'],
                        role=user_data['role']
                    )
                    db.session.add(user)
                    db.session.flush()  # Get user.id
                    
                    # Create student
                    student = Student(
                        id=user.id,
                        name=student_data['name'],
                        email=student_data['email'],
                        phone=student_data['phone'],
                        address=student_data['address'],
                        student_id=student_data['student_id'],
                        enrollment_date=datetime.strptime(student_data['enrollment_date'], '%Y-%m-%d').date()
                    )
                    db.session.add(student)
                    
                    if i % 20 == 0:
                        print(f"   ✅ Inserted {i} students...")
                        db.session.commit()
                except Exception as e:
                    print(f"   ⚠️  Error inserting student {i}: {str(e)}")
                    db.session.rollback()
                    continue
            
            db.session.commit()
            print(f"✅ Inserted {Student.query.count()} students!")
            
            # Insert packages
            print("\n📥 Inserting packages...")
            for pkg_data in sample_data['packages']:
                package = Package(**pkg_data)
                db.session.add(package)
            db.session.commit()
            print(f"✅ Inserted {Package.query.count()} packages!")
            
            # Insert subscriptions
            print("\n📥 Inserting subscriptions...")
            for sub_data in sample_data['subscriptions']:
                # Convert date strings to date objects for SQLite
                sub_data_copy = sub_data.copy()
                sub_data_copy['start_date'] = datetime.strptime(sub_data['start_date'], '%Y-%m-%d').date()
                sub_data_copy['end_date'] = datetime.strptime(sub_data['end_date'], '%Y-%m-%d').date()
                subscription = Subscription(**sub_data_copy)
                db.session.add(subscription)
            db.session.commit()
            print(f"✅ Inserted {Subscription.query.count()} subscriptions!")
            
            # Insert attendance
            print("\n📥 Inserting attendance records...")
            batch_size = 100
            for i, att_data in enumerate(sample_data['attendance'], 1):
                try:
                    # Convert date string to date object for SQLite
                    att_data_copy = att_data.copy()
                    att_data_copy['date'] = datetime.strptime(att_data['date'], '%Y-%m-%d').date()
                    attendance = Attendance(**att_data_copy)
                    db.session.add(attendance)
                    if i % batch_size == 0:
                        db.session.commit()
                        print(f"   ✅ Inserted {i} attendance records...")
                except Exception as e:
                    # Skip duplicates (unique constraint)
                    continue
            db.session.commit()
            print(f"✅ Inserted {Attendance.query.count()} attendance records!")
            
            # Insert feedbacks
            print("\n📥 Inserting feedbacks...")
            for fb_data in sample_data['feedbacks']:
                # Convert created_at string to datetime object for SQLite
                fb_data_copy = fb_data.copy()
                if 'created_at' in fb_data_copy and isinstance(fb_data_copy['created_at'], str):
                    fb_data_copy['created_at'] = datetime.fromisoformat(fb_data_copy['created_at'].replace('Z', '+00:00'))
                feedback = Feedback(**fb_data_copy)
                db.session.add(feedback)
            db.session.commit()
            print(f"✅ Inserted {Feedback.query.count()} feedbacks!")
            
            # Insert menu items
            print("\n📥 Inserting menu items...")
            for menu_data in sample_data['menu_items']:
                menu_item = MenuItem(**menu_data)
                db.session.add(menu_item)
            db.session.commit()
            print(f"✅ Inserted {MenuItem.query.count()} menu items!")
            
            # Create admin user
            if not User.query.filter_by(username='admin').first():
                admin_user = User(
                    username='admin',
                    password=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.flush()
                
                admin = Admin(
                    id=admin_user.id,
                    name='Admin User',
                    email='admin@smartmess.com',
                    phone='1234567890',
                    admin_id='A001',
                    permissions='{"all": true}'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created! (username: admin, password: admin123)")
            
            print("\n" + "=" * 50)
            print("🎉 Database setup complete!")
            print("=" * 50)
            print(f"\n📊 Database Statistics:")
            print(f"   - Users: {User.query.count()}")
            print(f"   - Students: {Student.query.count()}")
            print(f"   - Packages: {Package.query.count()}")
            print(f"   - Subscriptions: {Subscription.query.count()}")
            print(f"   - Attendance Records: {Attendance.query.count()}")
            print(f"   - Feedbacks: {Feedback.query.count()}")
            print(f"   - Menu Items: {MenuItem.query.count()}")
            print("\n✅ Ready to use! Run: python app.py")
    else:
        print("\n☁️  Using Supabase Database (Cloud)")
        print("=" * 50)
        print("\n⚠️  Supabase setup requires manual SQL execution.")
        print("Please run the SQL from create_tables_sql() in your Supabase SQL editor.")
        print("\nThen use the import script to populate data.")

if __name__ == '__main__':
    setup_supabase_database()

