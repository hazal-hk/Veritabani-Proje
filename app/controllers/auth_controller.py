from flask import Blueprint, request, jsonify
from app.services import auth_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity 

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

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    The user updates their profile.
    ---
    tags:
      - Authentication
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer <TOKEN>
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "yeni_email@ktu.edu.tr"
    responses:
      200:
        description: Profile updated
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    #kullanıcıyı bul emaili güncelle
    from app.models.user import User
    from app import db
    
    user = User.query.get(current_user_id)
    if 'email' in data:
        user.email = data['email']
        db.session.commit()
        
    return jsonify({'message': 'Profile updated', 'user': user.to_json()}), 200
