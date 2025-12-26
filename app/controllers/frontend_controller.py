from flask import Blueprint, render_template

#bunlar ana sayfalar olacak
frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    return render_template('login.html')

@frontend_bp.route('/login')
def login_page():
    return render_template('login.html')

@frontend_bp.route('/register')
def register_page():
    return render_template('register.html')

@frontend_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')