"""Quick script to add feedbacks"""
from app import app, db, Feedback
from datetime import datetime, timedelta
import random

feedback_texts = [
    'Great food quality!', 'Excellent service', 'Could improve variety',
    'Very satisfied', 'Good value for money', 'Needs more vegetarian options',
    'Amazing experience', 'Food was cold', 'Best mess service ever!',
    'Needs improvement in timing'
]

with app.app_context():
    # Get existing feedback count
    existing = Feedback.query.count()
    print(f"Existing feedbacks: {existing}")
    
    # Add feedbacks for students 1-60
    added = 0
    for i in range(1, 61):
        try:
            # Check if feedback already exists for this student
            if Feedback.query.filter_by(student_id=i).first():
                continue
            
            fb = Feedback(
                student_id=i,
                feedback_text=random.choice(feedback_texts),
                rating=random.randint(3, 5),
                created_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            db.session.add(fb)
            added += 1
        except Exception as e:
            print(f"Error adding feedback for student {i}: {e}")
            continue
    
    db.session.commit()
    print(f"✅ Added {added} feedbacks!")
    print(f"Total feedbacks: {Feedback.query.count()}")

