import jwt
import datetime
from flask import current_app
from app.repositories import user_repository

def register_user_service(data):
    if user_repository.find_user_by_username(data['username']):
        raise Exception('Username already exists')

    user = user_repository.save_new_user(data)
    return user.to_json()

def login_user_service(data):
    user = user_repository.find_user_by_username(data['username'])

    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    raise Exception('Invalid username or password')

