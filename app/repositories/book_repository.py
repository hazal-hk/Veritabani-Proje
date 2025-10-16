from unicodedata import category

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
                    publication_year=data.get['publication_year'],
                    category=data['category'],
    )
    db.session.add(new_book)
    db.session.commit()
    return new_book

#güncelleme
def update_book_db(book, data):
    book.title = data['title']
    book.isbn = data['isbn']
    book.author = data['author']
    book.publication_year = data['publication_year']
    book.category = data['category']

    db.session.commit()
    return book

#silme
def delete_book_db(book):
    db.session.delete(book)
    db.session.commit()
