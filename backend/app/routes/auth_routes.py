# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.models.User import User
from app.extensions import login_manager

auth_bp = Blueprint('auth_bp', __name__)

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)  # Use Flask-Login to log the user in
        return jsonify({"token": "fake-jwt-token"}), 200  # Replace with actual token generation
    return jsonify({"msg": "Invalid credentials"}), 401

# Logout route
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logged out"}), 200
