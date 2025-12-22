from app import db
from app.models.user import User

def get_user_by_username(username):
    #bu kullanıcı adı var mı diye bakar
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    #bundan var mı diye bakar
    return User.query.filter_by(email=email).first()

def save_new_user(user_data):
    #yeni bir kullanıcı oluşturur
    new_user = User(
        username=user_data['username'],
        email=user_data['email'],
        role=user_data.get('role', 'student') 
    )
    #şfreyi şifreleyerek(??) kaydeder 
    new_user.set_password(user_data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

