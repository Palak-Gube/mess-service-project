"""
Data Import Script - Import 500 rows into mess_service.db
Supports: CSV, SQL, Excel formats
"""
import sys
import io
import csv
from datetime import datetime, date
from werkzeug.security import generate_password_hash

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app, db, User, Student, Admin, Package, Subscription, Attendance, Feedback, MenuItem

def import_from_csv(csv_file_path, table_name='students'):
    """
    Import data from CSV file
    
    CSV Format for Students:
    name,email,phone,address,student_id,username,password,enrollment_date
    
    Example:
    John Doe,john@example.com,1234567890,123 Main St,S001,john_doe,password123,2024-01-01
    """
    print(f"\n📥 Importing {table_name} from CSV: {csv_file_path}")
    
    with app.app_context():
        imported_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    try:
                        if table_name == 'students':
                            # Check if username already exists
                            username = row.get('username', '').strip()
                            if not username:
                                username = f"student_{row.get('student_id', row_num)}"
                            
                            if User.query.filter_by(username=username).first():
                                print(f"  ⚠️  Row {row_num}: Username '{username}' already exists, skipping...")
                                skipped_count += 1
                                continue
                            
                            # Check if email already exists
                            email = row.get('email', '').strip()
                            if email and Student.query.filter_by(email=email).first():
                                print(f"  ⚠️  Row {row_num}: Email '{email}' already exists, skipping...")
                                skipped_count += 1
                                continue
                            
                            # Create user
                            password = row.get('password', 'password123').strip()
                            user = User(
                                username=username,
                                password=generate_password_hash(password),
                                role='student'
                            )
                            db.session.add(user)
                            db.session.flush()  # Get user.id
                            
                            # Parse enrollment date
                            enrollment_date_str = row.get('enrollment_date', '').strip()
                            if enrollment_date_str:
                                try:
                                    enrollment_date = datetime.strptime(enrollment_date_str, '%Y-%m-%d').date()
                                except:
                                    enrollment_date = date.today()
                            else:
                                enrollment_date = date.today()
                            
                            # Create student
                            student = Student(
                                id=user.id,
                                name=row.get('name', '').strip() or f"Student {row_num}",
                                email=email or f"student{row_num}@example.com",
                                phone=row.get('phone', '').strip(),
                                address=row.get('address', '').strip(),
                                student_id=row.get('student_id', '').strip() or f"S{user.id}",
                                enrollment_date=enrollment_date
                            )
                            db.session.add(student)
                            
                            imported_count += 1
                            if imported_count % 50 == 0:
                                print(f"  ✅ Imported {imported_count} students...")
                                db.session.commit()
                        
                        elif table_name == 'menu_items':
                            # Import menu items
                            menu_date_str = row.get('date', '').strip()
                            if menu_date_str:
                                try:
                                    menu_date = datetime.strptime(menu_date_str, '%Y-%m-%d').date()
                                except:
                                    menu_date = date.today()
                            else:
                                menu_date = date.today()
                            
                            menu_item = MenuItem(
                                name=row.get('name', '').strip(),
                                description=row.get('description', '').strip(),
                                category=row.get('category', 'Main Course').strip(),
                                price=float(row.get('price', 0) or 0),
                                date=menu_date,
                                image_path=row.get('image_path', '').strip()
                            )
                            db.session.add(menu_item)
                            imported_count += 1
                        
                        elif table_name == 'packages':
                            # Import packages
                            package = Package(
                                name=row.get('name', '').strip(),
                                price=float(row.get('price', 0) or 0),
                                duration_days=int(row.get('duration_days', 1) or 1),
                                features=row.get('features', '[]').strip(),
                                description=row.get('description', '').strip()
                            )
                            db.session.add(package)
                            imported_count += 1
                    
                    except Exception as e:
                        print(f"  ❌ Row {row_num}: Error - {str(e)}")
                        skipped_count += 1
                        continue
                
                # Final commit
                db.session.commit()
                
                print(f"\n✅ Import complete!")
                print(f"   Imported: {imported_count} rows")
                print(f"   Skipped: {skipped_count} rows")
                return imported_count
        
        except FileNotFoundError:
            print(f"❌ Error: File '{csv_file_path}' not found!")
            return 0
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error importing: {str(e)}")
            return 0

def import_from_sql(sql_file_path):
    """
    Import data from SQL file
    
    SQL Format:
    INSERT INTO students (id, name, email, phone, address, student_id, enrollment_date)
    VALUES (1, 'John Doe', 'john@example.com', '1234567890', '123 Main St', 'S001', '2024-01-01');
    """
    print(f"\n📥 Importing from SQL file: {sql_file_path}")
    
    with app.app_context():
        try:
            import sqlite3
            
            # Connect to existing database
            conn = sqlite3.connect('mess_service.db')
            cursor = conn.cursor()
            
            # Read SQL file
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Execute SQL (split by semicolons)
            statements = [s.strip() for s in sql_script.split(';') if s.strip()]
            
            executed = 0
            for statement in statements:
                try:
                    cursor.execute(statement)
                    executed += 1
                    if executed % 50 == 0:
                        print(f"  ✅ Executed {executed} statements...")
                except Exception as e:
                    print(f"  ⚠️  Skipped statement: {str(e)}")
                    continue
            
            conn.commit()
            conn.close()
            
            print(f"\n✅ SQL import complete! Executed {executed} statements")
            return executed
        
        except FileNotFoundError:
            print(f"❌ Error: File '{sql_file_path}' not found!")
            return 0
        except Exception as e:
            print(f"❌ Error importing SQL: {str(e)}")
            return 0

def import_from_excel(excel_file_path, sheet_name='Students'):
    """
    Import data from Excel file
    
    Requires: pip install openpyxl
    """
    print(f"\n📥 Importing from Excel: {excel_file_path}")
    
    try:
        import openpyxl
    except ImportError:
        print("❌ Error: openpyxl not installed!")
        print("   Install it with: pip install openpyxl")
        return 0
    
    with app.app_context():
        try:
            workbook = openpyxl.load_workbook(excel_file_path)
            sheet = workbook[sheet_name]
            
            # Get headers (first row)
            headers = [cell.value for cell in sheet[1]]
            
            imported_count = 0
            skipped_count = 0
            
            # Process rows (skip header)
            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # Create dictionary from row
                    row_dict = dict(zip(headers, row))
                    
                    # Skip empty rows
                    if not any(row_dict.values()):
                        continue
                    
                    # Check if username exists
                    username = str(row_dict.get('username', '')).strip()
                    if not username:
                        username = f"student_{row_dict.get('student_id', row_num)}"
                    
                    if User.query.filter_by(username=username).first():
                        skipped_count += 1
                        continue
                    
                    # Create user
                    password = str(row_dict.get('password', 'password123')).strip()
                    user = User(
                        username=username,
                        password=generate_password_hash(password),
                        role='student'
                    )
                    db.session.add(user)
                    db.session.flush()
                    
                    # Parse date
                    enrollment_date_str = str(row_dict.get('enrollment_date', '')).strip()
                    if enrollment_date_str:
                        try:
                            if isinstance(enrollment_date_str, datetime):
                                enrollment_date = enrollment_date_str.date()
                            else:
                                enrollment_date = datetime.strptime(enrollment_date_str, '%Y-%m-%d').date()
                        except:
                            enrollment_date = date.today()
                    else:
                        enrollment_date = date.today()
                    
                    # Create student
                    student = Student(
                        id=user.id,
                        name=str(row_dict.get('name', '')).strip() or f"Student {row_num}",
                        email=str(row_dict.get('email', '')).strip() or f"student{row_num}@example.com",
                        phone=str(row_dict.get('phone', '')).strip(),
                        address=str(row_dict.get('address', '')).strip(),
                        student_id=str(row_dict.get('student_id', '')).strip() or f"S{user.id}",
                        enrollment_date=enrollment_date
                    )
                    db.session.add(student)
                    
                    imported_count += 1
                    if imported_count % 50 == 0:
                        print(f"  ✅ Imported {imported_count} students...")
                        db.session.commit()
                
                except Exception as e:
                    print(f"  ⚠️  Row {row_num}: {str(e)}")
                    skipped_count += 1
                    continue
            
            db.session.commit()
            print(f"\n✅ Excel import complete!")
            print(f"   Imported: {imported_count} rows")
            print(f"   Skipped: {skipped_count} rows")
            return imported_count
        
        except FileNotFoundError:
            print(f"❌ Error: File '{excel_file_path}' not found!")
            return 0
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error importing Excel: {str(e)}")
            return 0

def create_sample_csv(filename='students_sample.csv', num_rows=500):
    """
    Create a sample CSV file with the correct format
    """
    print(f"\n📝 Creating sample CSV file: {filename}")
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'name', 'email', 'phone', 'address', 'student_id', 
            'username', 'password', 'enrollment_date'
        ])
        
        # Write sample rows
        for i in range(1, num_rows + 1):
            writer.writerow([
                f'Student {i}',
                f'student{i}@example.com',
                f'1234567{i:04d}',
                f'{i} Main Street',
                f'S{i:04d}',
                f'student{i}',
                'password123',
                '2024-01-01'
            ])
    
    print(f"✅ Created {filename} with {num_rows} rows")
    print(f"   You can edit this file and import it using:")
    print(f"   python import_data.py --csv {filename}")

def main():
    """Main function to handle command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import data into mess_service.db')
    parser.add_argument('--csv', type=str, help='Import from CSV file')
    parser.add_argument('--sql', type=str, help='Import from SQL file')
    parser.add_argument('--excel', type=str, help='Import from Excel file')
    parser.add_argument('--table', type=str, default='students', 
                       help='Table name (students, menu_items, packages)')
    parser.add_argument('--create-sample', action='store_true', 
                       help='Create sample CSV file')
    parser.add_argument('--rows', type=int, default=500, 
                       help='Number of rows for sample CSV')
    
    args = parser.parse_args()
    
    # Initialize database if needed
    with app.app_context():
        db.create_all()
        print("✅ Database tables ready!")
    
    if args.create_sample:
        create_sample_csv('students_sample.csv', args.rows)
        return
    
    if args.csv:
        import_from_csv(args.csv, args.table)
    elif args.sql:
        import_from_sql(args.sql)
    elif args.excel:
        import_from_excel(args.excel)
    else:
        print("\n📋 Data Import Tool")
        print("=" * 50)
        print("\nUsage:")
        print("  python import_data.py --csv students.csv")
        print("  python import_data.py --sql data.sql")
        print("  python import_data.py --excel data.xlsx")
        print("  python import_data.py --create-sample --rows 500")
        print("\nCSV Format (students):")
        print("  name,email,phone,address,student_id,username,password,enrollment_date")
        print("\nExample:")
        print("  John Doe,john@example.com,1234567890,123 Main St,S001,john_doe,pass123,2024-01-01")

if __name__ == '__main__':
    main()

