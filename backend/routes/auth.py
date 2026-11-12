from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from backend.extensions import db
from backend.models.user import User
from backend.utils.helpers import api_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('register.html')

@auth_bp.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or request.form
    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')
    remember = bool(data.get('remember', False))

    if not username_or_email or not password:
        return api_response(False, message="Username/Email and Password are required.", status_code=400)

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return api_response(False, message="Invalid username or password.", status_code=401)

    login_user(user, remember=remember)
    return api_response(True, data={'user': user.to_dict(), 'redirect': url_for('main.dashboard')}, message="Login successful!")

@auth_bp.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or request.form
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    full_name = data.get('full_name', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not username or not email or not password:
        return api_response(False, message="Username, email, and password are required.", status_code=400)

    if len(username) < 3:
        return api_response(False, message="Username must be at least 3 characters long.", status_code=400)

    if len(password) < 6:
        return api_response(False, message="Password must be at least 6 characters long.", status_code=400)

    if confirm_password and password != confirm_password:
        return api_response(False, message="Passwords do not match.", status_code=400)

    if User.query.filter_by(username=username).first():
        return api_response(False, message="Username is already taken.", status_code=409)

    if User.query.filter_by(email=email).first():
        return api_response(False, message="Email is already registered.", status_code=409)

    user = User(
        username=username,
        email=email,
        full_name=full_name or username
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Automatically log the user in
    login_user(user)

    return api_response(True, data={'user': user.to_dict(), 'redirect': url_for('main.dashboard')}, message="Registration successful! Welcome to AI Study Mate.")

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/api/auth/me', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return api_response(True, data={'user': current_user.to_dict(), 'authenticated': True})
    return api_response(True, data={'authenticated': False})
