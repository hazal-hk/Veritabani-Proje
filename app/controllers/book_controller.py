from flask import Blueprint, request, jsonify
from app.services import book_service

#bluprint oluştuturp tüm endpointlerin bu yolla başlaması için
books_bp = Blueprint('books_bp', __name__, url_prefix='/api/books')

@books_bp.route('/books', methods=['GET'])
def get_books():
    try:
        books = book_service.get_all_books_services()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/', methods=['POST'])

def create_book():
    data = request.get_json()

    if not data or not 'title' in data or not 'author' in data or not 'isbn' in data:
        return jsonify({'error': 'Missing data'}), 400

    try:
        new_book = book_service.create_book_service(data)
        return jsonify(new_book.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 409
