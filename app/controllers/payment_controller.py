from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import payment_service
from flasgger import swag_from

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/api/payments')

# cezaları gör
@payment_bp.route('/my-fines', methods=['GET'])
@jwt_required()
def get_my_fines():
    """
    Lists the user's unpaid fines.
    ---
    tags:
      - Payments
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer <TOKEN>
    responses:
      200:
        description: Penalty list
    """
    current_user_id = get_jwt_identity()
    fines = payment_service.get_my_fines_service(current_user_id)
    return jsonify(fines), 200

# ödeme yab
@payment_bp.route('/pay', methods=['POST'])
@jwt_required()
def pay_fine():
    """
    paying fines with a credit card
    ---
    tags:
      - Payments
    consumes:
      - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Bearer <TOKEN_HEREEEE>"
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - fine_id
            - card_number
            - expire_month
            - expire_year
            - cvc
          properties:
            fine_id:
              type: integer
              example: 1
            card_number:
              type: string
              example: "5528790000000001"
            expire_month:
              type: string
              example: "12"
            expire_year:
              type: string
              example: "2030"
            cvc:
              type: string
              example: "123"
            card_holder_name:
              type: string
              example: "Hazal Karayigit"
    responses:
      200:
        description: Payment successful
      400:
        description: Error
    """
    current_user_id = get_jwt_identity()
    
    #415 hatası için alınan çözüm
    # force=True: Header ne olursa olsun okur.
    # silent=True: Hata varsa patlamaz, None döner.
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({'error': 'Please submit valid JSON data (the Body part cannot be empty).'}), 400
    
    try:
        #data['fine_id'] yerine data.get('fine_id') yazmak daha güvewnliymiş
        result = payment_service.pay_fine_service(current_user_id, data.get('fine_id'), data)
        return jsonify({'message': 'Payment successful', 'fine': result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400