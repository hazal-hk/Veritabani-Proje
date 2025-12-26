from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import loan_service
from flasgger import swag_from

loan_bp = Blueprint('loan_bp', __name__, url_prefix='/api/loans')

#ödünç alma
@loan_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    """
    The user borrows a book.
    ---
    tags:
      - Library Operations
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
          required:
            - book_id
          properties:
            book_id:
              type: integer
              example: 1
    responses:
      200:
        description: Book received
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        result = loan_service.borrow_book_service(current_user_id, data['book_id'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

#kitabı iade etme
@loan_bp.route('/return', methods=['POST'])
@jwt_required()
def return_book():
    """
    The book will be returned (a penalty will be imposed if there is a delay)
    ---
    tags:
      - Library Operations
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
          required:
            - book_id
          properties:
            book_id:
              type: integer
              example: 1
    responses:
      200:
        description: Return successful
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        result = loan_service.return_book_service(current_user_id, data['book_id'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400