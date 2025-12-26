from app import db
from app.models.loan import Loan
from datetime import datetime, timedelta

def create_loan(user_id, book_id, days_to_return=15):
    #bugün aldın 15 gün sonra geri getirceksin
    due_date = datetime.utcnow() + timedelta(days=days_to_return)
    
    new_loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date)
    db.session.add(new_loan)
    db.session.commit()
    return new_loan

def get_active_loan(user_id, book_id):
    #henüz iadesini yapmadığı bir kaydı var mı?
    return Loan.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()

def return_loan_db(loan):
    loan.return_date = datetime.utcnow()
    db.session.commit()
    return loan