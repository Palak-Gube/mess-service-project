"""
Database initialization script
Run this once to create the database and add sample data
"""
import sys
import io
# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app, db, User, Student, Admin, Package, MenuItem
from werkzeug.security import generate_password_hash
from datetime import date

with app.app_context():
    # Create all tables
    db.create_all()
    print("[OK] Database tables created!")
    
    # Create sample packages
    if Package.query.count() == 0:
        packages = [
            Package(name='Basic Daily', price=100, duration_days=1, 
                   features='["Breakfast", "Lunch", "Dinner"]', 
                   description='Essential meals for a day.'),
            Package(name='Premium Weekly', price=600, duration_days=7, 
                   features='["Breakfast", "Lunch", "Dinner", "Snacks"]', 
                   description='Full week with extras.'),
            Package(name='VIP Monthly', price=2500, duration_days=30, 
                   features='["All meals", "Beverages", "Priority seating"]', 
                   description='Complete monthly plan with perks.')
        ]
        db.session.add_all(packages)
        print("[OK] Sample packages added!")
    
    # Create sample admin (optional)
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
        print("[OK] Sample admin created! (username: admin, password: admin123)")
    
    # Create sample student (optional)
    if not User.query.filter_by(username='student1').first():
        student_user = User(
            username='student1',
            password=generate_password_hash('student123'),
            role='student'
        )
        db.session.add(student_user)
        db.session.flush()
        
        student = Student(
            id=student_user.id,
            name='John Doe',
            email='john@example.com',
            phone='9876543210',
            address='123 College Street',
            student_id='S001'
        )
        db.session.add(student)
        print("[OK] Sample student created! (username: student1, password: student123)")
    
    db.session.commit()
    print("\n[SUCCESS] Database initialized successfully!")
    print("\nSample credentials:")
    print("Admin: username='admin', password='admin123'")
    print("Student: username='student1', password='student123'")

