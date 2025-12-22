from app.repositories import book_repository

#tüm kitapları çağırıp sonucu jsona çevirir
def get_all_books_services():
    books_from_db = book_repository.get_all_books()
    return [book.to_json() for book in books_from_db]

#read
def get_book_by_id_service(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        raise ValueError('Book not found')
    return book.to_json()
    if not data or 'title' not in data or 'isbn' not in data:
        raise ValueError("Title and ISBN are required!")

#yeni kitap için gerekenleri çağırır
def create_book_service(data):
    if not data or 'title' not in data or 'author' not in data or 'isbn' not in data:
        raise ValueError('Book not found')
#her şey yolundaysa yeni kitabı kaydeder
    new_book = book_repository.save_new_book(data)
    return new_book.to_json()

#güncelleme
def update_book_service(book_id, data):
    book_to_update = book_repository.get_book_by_id(book_id)
    if not book_to_update:
        raise ValueError('Book not found')

    updated_book = book_repository.update_book_db(book_to_update, data)
    return updated_book.to_json()

#silme
def delete_book_service(book_id):
    book_to_delete = book_repository.get_book_by_id(book_id)
    if not book_to_delete:
        raise ValueError('Book not found')

    book_repository.delete_book_db(book_to_delete)
    return True
