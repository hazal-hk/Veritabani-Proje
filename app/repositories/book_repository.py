from unicodedata import category
from sqlalchemy.exc import IntegrityError
from app.models.book import Book
from app import db

#veritabanındaki tüm kitapları getirir
def get_all_books():
    return Book.query.all()

#id'ye göre kitabı getirir
def get_book_by_id(book_id):
    return Book.query.get(book_id)

#yeni kitap kaydı
def save_new_book(data):
    new_book = Book(
        title=data['title'],
        isbn=data['isbn'],
        author=data['author'],
        publication_year=data.get('publication_year'),
        category=data['category']
    )
    
    try:
        db.session.add(new_book)
        db.session.commit()
    except IntegrityError:
        # hata olursa işlemi geri al (veritabanı kilitlenmesin diye)
        db.session.rollback()
        # o kocaman hata mesajı yerine bunu yazdır
        raise ValueError(f"A book with this ISBN ({data['isbn']}) number is already registered!!!!!")
        
    return new_book

#güncelleme
def update_book_db(book, data):
#geldiyse güncelle
    if 'title' in data:
        book.title = data['title']
    
    if 'author' in data:
        book.author = data['author']
        
    if 'isbn' in data:
        book.isbn = data['isbn']
        
    if 'category' in data:
        book.category = data['category']

    if 'publication_year' in data:
        book.publication_year = data['publication_year']

    if 'status' in data:
        book.status = data['status']

    db.session.commit()
    return book

#silme
def delete_book_db(book):
    db.session.delete(book)
    db.session.commit()
