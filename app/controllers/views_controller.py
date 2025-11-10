from flask import Blueprint, render_template

views_bp = Blueprint('views_bp', __name__)

@views_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@views_bp.route('/books', methods=['GET'])
def books_page():
    return render_template('books.html')

@views_bp.route('/admin', methods=['GET'])
def admin_page():
    return render_template('admin.html')