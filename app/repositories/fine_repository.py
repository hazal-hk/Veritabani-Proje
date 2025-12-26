from app import db
from app.models.fine import Fine

def create_fine(user_id, amount, reason):
    new_fine = Fine(user_id=user_id, amount=amount, reason=reason)
    db.session.add(new_fine)
    db.session.commit()
    return new_fine

def get_user_fines(user_id):
    # sadece ödenmemiş cezaları seçer
    return Fine.query.filter_by(user_id=user_id, is_paid=False).all()

def get_fine_by_id(fine_id):
    return Fine.query.get(fine_id)

def pay_fine_db(fine):
    fine.is_paid = True
    db.session.commit()
    return fine