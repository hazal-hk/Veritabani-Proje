from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
swagger = Swagger()

def create_app():
    app = Flask(__name__)

    #Kullanıcı: noos_user
    #sifre: admin123
    #sunucu: localhost
    #veritabani: akilli_kutuphane_db


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://noos_user:admin123@localhost/akilli_kutuphane_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    mail.init_app(app)
    swagger.init_app(app)

    from app.controllers.book_controller import books_bp
    app.register_blueprint(books_bp)

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from app.controllers.views_controller import views_bp
    app.register_blueprint(views_bp)

    return app