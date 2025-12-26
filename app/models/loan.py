from app import db
from datetime import datetime, timedelta

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow) #alış tarihi
    due_date = db.Column(db.DateTime, nullable=False) #son teslim
    return_date = db.Column(db.DateTime, nullable=True) #iade ettiği tarih ilk başta boş o yüzden nullable true oldu
    
    #veritabanı için ilişkiler
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    # Backref ile User ve Book üzerinden erişim
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'book': self.book.title,
            'book_id': self.book.id,  #BURAYI NASI UNUTTUN İDSİZ OLUR MU
            'borrow_date': self.borrow_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'is_returned': self.return_date is not None
        }