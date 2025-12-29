from app.repositories import book_repository
from app.models.loan import Loan

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
#force=False varsayılan değerini ekledim çünkü önce bi sorsun admin okeylerse force true olsun
def delete_book_service(book_id, force=False):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        raise ValueError("Book not found")
    
    #ödünç var mı
    existing_loan = Loan.query.filter_by(book_id=book_id).first()
    
    if existing_loan:
        #eger varsa VE zorlama yoksa hata tükür
        if not force:
            raise ValueError("CONFIRM_REQUIRED: This book has active or past loan records!")
        
        #eğer kayıt var VE force=True ise temizle
        else:
            Loan.query.filter_by(book_id=book_id).delete()
            db.session.flush() #commit öncesi temizlik
            
    #SİLLLLL
    book_repository.delete_book_db(book)