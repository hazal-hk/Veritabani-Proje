from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_mail import Mail
from flask_jwt_extended import JWTManager
import os
import datetime

db = SQLAlchemy()
mail = Mail()
swagger = Swagger()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    #Kullanıcı: noos_user
    #sifre: admin123
    #sunucu: localhost
    #veritabani: akilli_kutuphane_db


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://noos_user:admin123@localhost/akilli_kutuphane_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'varsayilan_guvenli_anahtar_123'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    #SÜREKLİ GİRİŞ YAPMAKLA UĞRAŞTIĞIM İÇİN TOKEN SÜRESİNİ ARTTIRDIM
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=7)

    # swagger için güvenlik ayarı template i
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "API Documentation",
            "version": "1.0.0"
        },
        #kilit butonunu oluşturan ayar
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your token here: Bearer <token>"
            }
        }
    }

    db.init_app(app)
    mail.init_app(app)
    # template i init_app içinde değil doğrudan nesnesine
    swagger.template = swagger_template
    swagger.init_app(app)

    jwt.init_app(app)

    from app.controllers.book_controller import books_bp
    app.register_blueprint(books_bp)

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from app.controllers.views_controller import views_bp
    app.register_blueprint(views_bp)

    from app.models.fine import Fine

    return app