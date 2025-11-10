from app.models.user import User
from app import db

def find_user_by_username(username):
    return User.query.filter_by(username=username).first()

def save_new_user(data):
    new_user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'student')
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return new_user

