from app.repositories import book_repository

def get_all_books_services():
    books = book_repository.get_all_books()
    return [book.to_json() for book in books]

#yeni kitap için gerekenleri çağırır
def create_book_service(data):



    new_book = book_repository.save_new_book(data)
    return new_book.to_json()
