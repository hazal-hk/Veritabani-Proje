from flask import Blueprint, request, jsonify
from app.services import book_service
from app.services.book_service import delete_book_service
from flasgger import swag_from

#bluprint oluştuturp tüm endpointlerin bu yolla başlaması için
books_bp = Blueprint('books_bp', __name__, url_prefix='/api')

#tümünü listeleme
@books_bp.route('/books', methods=['GET'])
@swag_from('/home/eilrie/Documents/GitHub/Veritabani-Proje/app/docs/get_all_books.yml')
def get_books():
    try:
        books = book_service.get_all_books_services()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#id ile tek kitap getirme
@books_bp.route('/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    try:
        book = book_service.get_book_by_id_service(book_id)
        return jsonify(book), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

#yeni oluşturma
@books_bp.route('/', methods=['POST'])
@swag_from('/home/eilrie/Documents/GitHub/Veritabani-Proje/app/docs/create_books.yml')
def create_book():
    data = request.get_json()

    if not data or not 'title' in data or not 'author' in data or not 'isbn' in data:
        return jsonify({'error': 'Missing data'}), 400

    try:
        new_book = book_service.create_book_service(data)
        return jsonify(new_book.to_json()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

#id ile bir tanesini güncelleme
@books_bp.route('/<int:book_id>', methods=['PUT'])
@swag_from('/home/eilrie/Documents/GitHub/Veritabani-Proje/app/docs/update_book.yml')
def update_book(book_id):
    data = request.get_json()
    try:
        updated_book = book_service.update_book_service(book_id, data)
        return jsonify(updated_book.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

#id ile bir tanesini silme
@books_bp.route('/<int:book_id>', methods=['DELETE'])
@swag_from('/home/eilrie/Documents/GitHub/Veritabani-Proje/app/docs/delete_book.yml')
def delete_book(book_id):
    try:
        delete_book_service(book_id)
        return jsonify({'deleted': True}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
