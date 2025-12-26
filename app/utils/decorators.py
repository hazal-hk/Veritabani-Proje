from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(required_role):
    """
    It prevents entry to those who do not have a specific role. Usage: @role_required('admin')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  #token var mı kontrol et
            claims = get_jwt()       #token içindeki gizli bilgiyi oku
            
            #token içindeki rol ile istenen rol mü
            if claims.get('role') != required_role:
                return jsonify(msg='You do not have permission to perform this action!'), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required():
    """Shortcut for Admin Only"""
    return role_required('admin')

def academician_required():
    """Shortcut for Academics Only"""
    return role_required('academician')