from flask import Blueprint, request, jsonify
from app.services import auth_service

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        new_user = auth_service.register_user_service(data)
        return jsonify(new_user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception:
        return jsonify({'error': 'There is an error during registration.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        token = auth_service.login_user_service(data)
        return jsonify({'token': token}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
