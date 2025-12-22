from flask import Blueprint, request, jsonify
from app.services import auth_service
from flasgger import swag_from

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@swag_from('../docs/register.yml') 
def register():
    data = request.get_json()
    
    try:
        new_user = auth_service.register_user_service(data)
        return jsonify({
            'message': 'User successfully created',
            'user': new_user.to_json()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Server error: ' + str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@swag_from('../docs/login.yml')
def login():
    data = request.get_json()
    try:
        result = auth_service.login_user_service(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
