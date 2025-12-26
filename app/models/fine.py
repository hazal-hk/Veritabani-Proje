from app import db
from datetime import datetime

class Fine(db.Model):
    __tablename__ = 'fines'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False) 
    reason = db.Column(db.String(255), nullable=False) 
    is_paid = db.Column(db.Boolean, default=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # bir ceza bir kullanıcınındır
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # cezayı tanımladım
    user = db.relationship('User', backref=db.backref('fines', lazy=True))

    def to_json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'reason': self.reason,
            'is_paid': self.is_paid,
            'created_at': self.created_at,
            'user_id': self.user_id
        }