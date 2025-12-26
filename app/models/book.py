from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    category = db.Column(db.String(50), nullable=False)

#bu fonksiyonu nesneyi json'a çevirmeyi kolaylaştırması için ekledim
def to_json(self):
    return {
        'id': self.id,
        'title': self.title,
        'isbn': self.isbn,
        'author': self.author,
        'publication_year': self.publication_year,
        'category': self.category,
    }