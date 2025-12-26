import jwt
import datetime
from flask import current_app
from app.repositories import user_repository
from flask_jwt_extended import create_access_token

def login_user_service(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise ValueError('Username and password are required')

    user = user_repository.get_user_by_username(username)

    if not user or not user.check_password(password):
        raise ValueError('invalid username or password')

    access_token = create_access_token(identity=str(user.id))

    return {
        'message' : 'login successful',
        'access_token' : access_token,
        'user' : user.to_json()
    }


def register_user_service(data):
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        raise ValueError('Username, email, and password are required.')

    if user_repository.get_user_by_username(data['username']):
        raise ValueError('This username is already in use')

    if user_repository.get_user_by_email(data['email']):
        raise ValueError('This email address is already registered')

    return user_repository.save_new_user(data)

def login_user_service(data):
    user = user_repository.get_user_by_username(data['username'])

    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    raise Exception('Invalid username or password')

