from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for frontend-backend communication

# Database Configuration - Supports both SQLite and Supabase
# To use Supabase, set environment variables:
# SUPABASE_URL=your-project-url
# SUPABASE_KEY=your-anon-key
# USE_SUPABASE=true

use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
supabase_url = os.getenv('SUPABASE_URL', '')
supabase_key = os.getenv('SUPABASE_KEY', '')

if use_supabase and supabase_url and supabase_key:
    # Use Supabase (PostgreSQL)
    # Format: postgresql://postgres:[password]@[host]:[port]/postgres
    # For Supabase, use connection pooling URL from project settings
    db_password = os.getenv('SUPABASE_DB_PASSWORD', '')
    db_host = supabase_url.replace('https://', '').replace('.supabase.co', '')
    if db_password:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres.{db_host}:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
    else:
        # Fallback to SQLite if Supabase credentials incomplete
        print("⚠️  Supabase credentials incomplete, using SQLite")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_service.db'
else:
    # Use SQLite (default)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_service.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """Authentication table - stores login credentials for students and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    admin = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')

class Student(db.Model):
    """Student details table"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date, default=date.today)
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='student', lazy=True, cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', backref='student', lazy=True, cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')

class Admin(db.Model):
    """Admin details for large-scale service providers"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.Column(db.Text)  # JSON string for permissions

class Feedback(db.Model):
    """All student feedbacks"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Package(db.Model):
    """Available meal packages"""
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text)  # JSON string for features
    description = db.Column(db.Text)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='package', lazy=True)

class Subscription(db.Model):
    """Student meal package subscriptions"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'expired', 'cancelled'
    amount_paid = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    """Daily meal attendance tracking"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # 'breakfast', 'lunch', 'dinner'
    marked_by = db.Column(db.String(50))  # admin_id or 'self'
    status = db.Column(db.String(20), default='present')  # 'present', 'absent'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one record per student per meal per day
    __table_args__ = (db.UniqueConstraint('student_id', 'date', 'meal_type', name='unique_attendance'),)

class MenuItem(db.Model):
    """Daily menu items"""
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # 'Main Course', 'Beverage', etc.
    price = db.Column(db.Float)
    date = db.Column(db.Date, default=date.today)
    image_path = db.Column(db.String(255))
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='menu_item', lazy=True)

# ==================== API ROUTES ====================

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint for students and admins"""
    data = request.json
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    
    if not all([role, username, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(username=username, role=role).first()
    if user and check_password_hash(user.password, password):
        return jsonify({
            'success': True,
            'user_id': user.id,
            'role': user.role,
            'message': 'Login successful'
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    """Register new student or admin"""
    try:
        data = request.json
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if not all([role, username, password]):
            return jsonify({'error': 'Missing required fields (role, username, password)'}), 400
        
        # Validate role
        if role not in ['student', 'admin']:
            return jsonify({'error': 'Invalid role. Must be "student" or "admin"'}), 400
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Validate email format if provided
        if email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email already exists
            if role == 'student' and Student.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already registered'}), 400
            elif role == 'admin' and Admin.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already registered'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check for duplicate student_id if provided (for students)
        if role == 'student':
            provided_student_id = data.get('student_id', '').strip()
            if provided_student_id:
                # Check if student_id already exists
                if Student.query.filter_by(student_id=provided_student_id).first():
                    return jsonify({'error': f'Student ID "{provided_student_id}" is already registered. Please use a different ID or leave it blank to auto-generate one.'}), 400
        
        # Check for duplicate admin_id if provided (for admins)
        if role == 'admin':
            provided_admin_id = data.get('admin_id', '').strip()
            if provided_admin_id:
                # Check if admin_id already exists
                if Admin.query.filter_by(admin_id=provided_admin_id).first():
                    return jsonify({'error': f'Admin ID "{provided_admin_id}" is already registered. Please use a different ID or leave it blank to auto-generate one.'}), 400
        
        # Create user
        user = User(
            username=username,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.flush()
        
        # Create student or admin record
        if role == 'student':
            # Generate unique student_id - it's required (NOT NULL in database)
            provided_student_id = data.get('student_id', '').strip()
            
            if provided_student_id:
                # Use provided student_id (already checked for duplicates above)
                student_id = provided_student_id
            else:
                # Auto-generate unique student_id if not provided
                # Try to find next available ID
                base_id = user.id
                student_id = f'S{base_id:05d}'
                
                # Ensure uniqueness - if auto-generated ID exists, find next available
                counter = 0
                while Student.query.filter_by(student_id=student_id).first():
                    counter += 1
                    student_id = f'S{base_id + counter:05d}'
                    # Safety check to prevent infinite loop
                    if counter > 1000:
                        student_id = f'S{int(datetime.now().timestamp())}'
                        break
            
            student = Student(
                id=user.id,
                name=data.get('name', ''),
                email=email,
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                student_id=student_id  # Always has a value - never null
            )
            db.session.add(student)
        elif role == 'admin':
            # Generate unique admin_id - it's required (NOT NULL in database)
            provided_admin_id = data.get('admin_id', '').strip()
            
            if provided_admin_id:
                # Use provided admin_id (already checked for duplicates above)
                admin_id = provided_admin_id
            else:
                # Auto-generate unique admin_id if not provided
                base_id = user.id
                admin_id = f'A{base_id:05d}'
                
                # Ensure uniqueness - if auto-generated ID exists, find next available
                counter = 0
                while Admin.query.filter_by(admin_id=admin_id).first():
                    counter += 1
                    admin_id = f'A{base_id + counter:05d}'
                    # Safety check to prevent infinite loop
                    if counter > 1000:
                        admin_id = f'A{int(datetime.now().timestamp())}'
                        break
            
            admin = Admin(
                id=user.id,
                name=data.get('name', ''),
                email=email,
                phone=data.get('phone', ''),
                admin_id=admin_id,  # Always has a value - never null
                permissions=data.get('permissions', '{}')
            )
            db.session.add(admin)
        
        db.session.commit()
        return jsonify({'success': True, 'user_id': user.id, 'message': 'Registration successful'})
    except Exception as e:
        db.session.rollback()
        # Provide more user-friendly error messages
        error_msg = str(e)
        if 'UNIQUE constraint failed: students.student_id' in error_msg:
            return jsonify({'error': 'This Student ID is already registered. Please use a different ID or leave it blank to auto-generate one.'}), 400
        elif 'UNIQUE constraint failed: students.email' in error_msg:
            return jsonify({'error': 'This email is already registered. Please use a different email address.'}), 400
        elif 'UNIQUE constraint failed: users.username' in error_msg:
            return jsonify({'error': 'This username is already taken. Please choose a different username.'}), 400
        else:
            return jsonify({'error': f'Registration failed: {error_msg}'}), 500

# Student endpoints
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get student profile"""
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'phone': student.phone,
        'address': student.address,
        'student_id': student.student_id
    })

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student profile"""
    student = Student.query.get_or_404(student_id)
    data = request.json
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.phone = data.get('phone', student.phone)
    student.address = data.get('address', student.address)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Profile updated'})

@app.route('/api/students/<int:student_id>/feedback', methods=['POST'])
def submit_feedback(student_id):
    """Submit student feedback"""
    data = request.json
    feedback = Feedback(
        student_id=student_id,
        feedback_text=data.get('feedback'),
        rating=data.get('rating'),
        menu_item_id=data.get('menu_item_id')
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Feedback submitted'})

@app.route('/api/students/<int:student_id>/subscriptions', methods=['GET'])
def get_student_subscriptions(student_id):
    """Get student's subscriptions"""
    subscriptions = Subscription.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': s.id,
        'package_name': s.package.name,
        'start_date': s.start_date.isoformat(),
        'end_date': s.end_date.isoformat(),
        'status': s.status,
        'amount_paid': s.amount_paid
    } for s in subscriptions])

@app.route('/api/students/<int:student_id>/subscriptions', methods=['POST'])
def create_subscription(student_id):
    """Student selects a meal package"""
    try:
        data = request.json
        package_id = data.get('packageId')
        
        if not package_id:
            return jsonify({'error': 'Package ID is required'}), 400
        
        package = Package.query.get(package_id)
        if not package:
            return jsonify({'error': 'Package not found'}), 404
        
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Calculate end date
        from datetime import timedelta
        start = date.today()
        end = start + timedelta(days=package.duration_days)
        
        subscription = Subscription(
            student_id=student_id,
            package_id=package_id,
            start_date=start,
            end_date=end,
            amount_paid=package.price,
            status='active'
        )
        db.session.add(subscription)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subscription created successfully', 'subscription_id': subscription.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>/attendance', methods=['POST'])
def mark_attendance(student_id):
    """Mark student attendance (self or admin)"""
    try:
        data = request.json
        att_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today()
        meal_type = data.get('mealType', 'lunch')
        
        # Check if attendance already exists
        existing = Attendance.query.filter_by(
            student_id=student_id,
            date=att_date,
            meal_type=meal_type
        ).first()
        
        if existing:
            return jsonify({'error': 'Attendance already marked for this meal today'}), 400
        
        attendance = Attendance(
            student_id=student_id,
            date=att_date,
            meal_type=meal_type,
            marked_by=data.get('marked_by', 'self'),
            status='present'
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance marked successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>/attendance', methods=['GET'])
def get_student_attendance(student_id):
    """Get student's attendance records"""
    records = Attendance.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'date': r.date.isoformat(),
        'meal_type': r.meal_type,
        'status': r.status
    } for r in records])

# Admin endpoints
@app.route('/api/admin/feedbacks', methods=['GET'])
def get_all_feedbacks():
    """Get all student feedbacks for admin"""
    feedbacks = Feedback.query.all()
    return jsonify([{
        'id': f.id,
        'student_name': f.student.name,
        'student_id': f.student.student_id,
        'feedback_text': f.feedback_text,
        'rating': f.rating,
        'created_at': f.created_at.isoformat()
    } for f in feedbacks])

@app.route('/api/admin/subscriptions', methods=['GET'])
def get_all_subscriptions():
    """Get all student subscriptions for admin"""
    subscriptions = Subscription.query.all()
    return jsonify([{
        'id': s.id,
        'student_name': s.student.name,
        'student_id': s.student.student_id,
        'package_name': s.package.name,
        'start_date': s.start_date.isoformat(),
        'end_date': s.end_date.isoformat(),
        'status': s.status,
        'amount_paid': s.amount_paid
    } for s in subscriptions])

@app.route('/api/admin/attendance', methods=['POST'])
def admin_mark_attendance():
    """Admin marks student attendance"""
    try:
        data = request.json
        student_id = data.get('studentId')
        if not student_id:
            return jsonify({'error': 'Student ID is required'}), 400
        
        att_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today()
        meal_type = data.get('mealType', 'lunch')
        
        # Check if attendance already exists
        existing = Attendance.query.filter_by(
            student_id=student_id,
            date=att_date,
            meal_type=meal_type
        ).first()
        
        if existing:
            return jsonify({'error': 'Attendance already marked for this student and meal'}), 400
        
        attendance = Attendance(
            student_id=student_id,
            date=att_date,
            meal_type=meal_type,
            marked_by=f"admin_{data.get('adminId', 'unknown')}",
            status='present'
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance marked by admin successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/attendance', methods=['GET'])
def get_attendance_report():
    """Get attendance report for a date"""
    att_date = request.args.get('date', date.today().isoformat())
    records = Attendance.query.filter_by(date=datetime.strptime(att_date, '%Y-%m-%d').date()).all()
    return jsonify([{
        'id': r.id,  # Include ID for update/delete operations
        'student_id': r.student_id,
        'student_name': r.student.name,
        'student_id_display': r.student.student_id,
        'meal_type': r.meal_type,
        'status': r.status,
        'date': r.date.isoformat(),
        'marked_by': r.marked_by
    } for r in records])

@app.route('/api/admin/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    """Update attendance record (Admin)"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        data = request.json
        
        attendance.status = data.get('status', attendance.status)
        attendance.meal_type = data.get('meal_type', attendance.meal_type)
        if data.get('date'):
            attendance.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    """Delete attendance record (Admin)"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    """Admin dashboard statistics"""
    try:
        from datetime import timedelta
        
        # Get selected student IDs from query parameters
        selected_students = request.args.get('student_ids', '')
        student_ids_list = []
        if selected_students:
            try:
                student_ids_list = [int(id.strip()) for id in selected_students.split(',') if id.strip()]
            except:
                student_ids_list = []
        
        # Auto-update expired subscriptions
        expired_subs = Subscription.query.filter(
            Subscription.status == 'active',
            Subscription.end_date < date.today()
        ).all()
        for sub in expired_subs:
            sub.status = 'expired'
        db.session.commit()
        
        total_students = Student.query.count()
        active_subscriptions = Subscription.query.filter_by(status='active').count()
        total_feedbacks = Feedback.query.count()
        today_attendance = Attendance.query.filter_by(date=date.today()).count()
        
        # Calculate pending payments (expired or cancelled subscriptions that haven't been renewed)
        pending_payments = db.session.query(db.func.sum(Subscription.amount_paid)).filter(
            Subscription.status.in_(['expired', 'cancelled'])
        ).scalar() or 0
        
        # Get feedbacks - filter by selected students if provided
        if student_ids_list:
            recent_feedbacks_query = Feedback.query.filter(Feedback.student_id.in_(student_ids_list)).order_by(Feedback.created_at.desc())
        else:
            recent_feedbacks_query = Feedback.query.order_by(Feedback.created_at.desc()).limit(5)
        recent_feedbacks = recent_feedbacks_query.all()
        feedbacks_list = [{
            'id': f.id,
            'student_name': f.student.name,
            'student_id': f.student.student_id,
            'feedback_text': f.feedback_text[:100] + '...' if len(f.feedback_text) > 100 else f.feedback_text,
            'rating': f.rating,
            'created_at': f.created_at.isoformat()
        } for f in recent_feedbacks]
        
        # Get subscriptions - filter by selected students if provided
        if student_ids_list:
            recent_subscriptions_query = Subscription.query.filter(Subscription.student_id.in_(student_ids_list)).order_by(Subscription.created_at.desc())
        else:
            recent_subscriptions_query = Subscription.query.order_by(Subscription.created_at.desc()).limit(5)
        recent_subscriptions = recent_subscriptions_query.all()
        subscriptions_list = [{
            'id': s.id,
            'student_name': s.student.name,
            'student_id': s.student.student_id,
            'package_name': s.package.name,
            'amount_paid': s.amount_paid,
            'status': s.status,
            'created_at': s.created_at.isoformat()
        } for s in recent_subscriptions]
        
        # Get attendance - filter by selected students if provided
        if student_ids_list:
            today_attendance_query = Attendance.query.filter(
                Attendance.date == date.today(),
                Attendance.student_id.in_(student_ids_list)
            )
        else:
            today_attendance_query = Attendance.query.filter_by(date=date.today())
        today_attendance_list = today_attendance_query.all()
        attendance_list = [{
            'student_name': a.student.name,
            'student_id': a.student.student_id,
            'meal_type': a.meal_type,
            'status': a.status
        } for a in today_attendance_list]
        
        # Weekly stats (last 7 days)
        week_start = date.today() - timedelta(days=7)
        weekly_feedbacks = Feedback.query.filter(Feedback.created_at >= week_start).count()
        weekly_subscriptions = Subscription.query.filter(Subscription.created_at >= week_start).count()
        weekly_attendance = Attendance.query.filter(Attendance.date >= week_start).count()
        weekly_revenue = db.session.query(db.func.sum(Subscription.amount_paid)).filter(
            Subscription.created_at >= week_start
        ).scalar() or 0
        
        # Daily attendance for last 7 days (for chart)
        daily_attendance_data = []
        for i in range(7):
            day = date.today() - timedelta(days=i)
            count = Attendance.query.filter_by(date=day).count()
            daily_attendance_data.append({
                'date': day.isoformat(),
                'count': count
            })
        daily_attendance_data.reverse()
        
        return jsonify({
            'total_students': total_students,
            'active_subscriptions': active_subscriptions,
            'total_feedbacks': total_feedbacks,
            'today_attendance': today_attendance,
            'pending_payments': pending_payments,
            'recent_feedbacks': feedbacks_list,
            'recent_subscriptions': subscriptions_list,
            'today_attendance_list': attendance_list,
            'weekly_stats': {
                'feedbacks': weekly_feedbacks,
                'subscriptions': weekly_subscriptions,
                'attendance': weekly_attendance,
                'revenue': weekly_revenue
            },
            'daily_attendance_chart': daily_attendance_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Menu & Packages endpoints
@app.route('/api/menu/today', methods=['GET'])
def get_today_menu():
    """Get today's menu"""
    menu_items = MenuItem.query.filter_by(date=date.today()).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'category': m.category,
        'price': m.price,
        'image_path': m.image_path
    } for m in menu_items])

@app.route('/api/packages', methods=['GET'])
def get_packages():
    """Get all available packages"""
    packages = Package.query.all()
    # Remove duplicates based on package ID (in case of database duplicates)
    seen_ids = set()
    unique_packages = []
    for p in packages:
        if p.id not in seen_ids:
            seen_ids.add(p.id)
            unique_packages.append(p)
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'duration': p.duration_days,
        'features': p.features,
        'description': p.description
    } for p in unique_packages])

# Additional Admin endpoints
@app.route('/api/admin/students', methods=['GET'])
def get_all_students():
    """Get all students for admin"""
    try:
        students = Student.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'phone': s.phone,
            'student_id': s.student_id,
            'subscription_status': 'Active' if Subscription.query.filter_by(student_id=s.id, status='active').first() else 'Inactive'
        } for s in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    """Get admin profile"""
    try:
        admin = Admin.query.get_or_404(admin_id)
        return jsonify({
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'phone': admin.phone,
            'admin_id': admin.admin_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription_status(subscription_id):
    """Update subscription status (e.g., mark as expired, cancelled)"""
    try:
        data = request.json
        status = data.get('status')
        
        if status not in ['active', 'expired', 'cancelled']:
            return jsonify({'error': 'Invalid status. Must be active, expired, or cancelled'}), 400
        
        subscription = Subscription.query.get_or_404(subscription_id)
        subscription.status = status
        db.session.commit()
        return jsonify({'success': True, 'message': f'Subscription marked as {status}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Menu Management endpoints
@app.route('/api/admin/menu', methods=['GET'])
def get_all_menu_items():
    """Get all menu items"""
    menu_items = MenuItem.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'category': m.category,
        'price': m.price,
        'date': m.date.isoformat() if m.date else None,
        'image_path': m.image_path
    } for m in menu_items])

@app.route('/api/admin/menu', methods=['POST'])
def create_menu_item():
    """Create a new menu item"""
    data = request.json
    menu_item = MenuItem(
        name=data.get('name'),
        description=data.get('description', ''),
        category=data.get('category', 'Main Course'),
        price=data.get('price', 0),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today(),
        image_path=data.get('image_path', '')
    )
    db.session.add(menu_item)
    db.session.commit()
    return jsonify({'success': True, 'id': menu_item.id, 'message': 'Menu item created'})

@app.route('/api/admin/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update a menu item"""
    menu_item = MenuItem.query.get_or_404(item_id)
    data = request.json
    menu_item.name = data.get('name', menu_item.name)
    menu_item.description = data.get('description', menu_item.description)
    menu_item.category = data.get('category', menu_item.category)
    menu_item.price = data.get('price', menu_item.price)
    if data.get('date'):
        menu_item.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Menu item updated'})

@app.route('/api/admin/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """Delete a menu item"""
    menu_item = MenuItem.query.get_or_404(item_id)
    db.session.delete(menu_item)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Menu item deleted'})

# Billing endpoints
@app.route('/api/students/<int:student_id>/bills', methods=['GET'])
def get_student_bills(student_id):
    """Get student's bills/payments"""
    subscriptions = Subscription.query.filter_by(student_id=student_id).all()
    bills = []
    for sub in subscriptions:
        bills.append({
            'id': sub.id,
            'description': f'{sub.package.name} Subscription',
            'amount': sub.amount_paid,
            'due_date': sub.end_date.isoformat(),
            'status': 'Paid' if sub.status == 'active' else 'Pending',
            'created_at': sub.created_at.isoformat()
        })
    return jsonify(bills)

# ==================== STATIC FILE ROUTES ====================
# These routes must come AFTER API routes to avoid conflicts

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (HTML, CSS, JS, images, etc.)"""
    # Don't serve API routes or internal files
    if filename.startswith('api/') or filename.startswith('__') or filename.startswith('venv/'):
        return jsonify({'error': 'Not found'}), 404
    # Only serve files that exist
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return jsonify({'error': 'File not found'}), 404

# Initialize database - run init_db.py instead

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

