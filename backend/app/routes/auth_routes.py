# routes/auth_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required
from app.models.User import User
from app.extensions import login_manager
from functools import wraps
from flask_jwt_extended import JWTManager
# from app import app

auth_bp = Blueprint('auth_bp', __name__)

jwt=JWTManager()


# get current route
# @auth_bp.route('/current_user')
# def token_required(f):
#   @wraps(f)
#   def decorated(*args, **kwargs):
#     token = None

#     # jwt is passed in the request header
#     if 'Authorization' in request.headers:
#       token = request.headers['Authorization'].split(" ")[1]

#     if not token:
#       return jsonify({'msg':'Token is msising!'}), 401

#     try:
#       # decode token to get user's id
#       data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms =['HS256'])
#       current_user = User.query.get(data['id'])
#     except Exception as e:
#        return jsonify({'msg':'Invalid token'}), 401

#     return f(current_user, *args, **kwargs)
#   return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            print("No token provided")
            return jsonify({'msg': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['id'])
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return jsonify({'msg': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print("Invalid token")
            return jsonify({'msg': 'Invalid token!'}), 401
        except Exception as e:
            print(f"Token decode error: {e}")
            return jsonify({'msg': 'Token is invalid!'}), 401

        if not current_user:
            print("User not found")
            return jsonify({'msg': 'User not found!'}), 404

        print(f"Current user: {current_user.username} (ID: {current_user.id})")
        return f(current_user, *args, **kwargs)

    return decorated

@auth_bp.route('/current_user', methods = ['GET'])
@token_required
def get_current_user(current_user):
    if not current_user:
        return jsonify({'msg':'user not found'}), 404


    print(f"Current user details: ID={current_user.id}, Username={current_user.username}")
    user_data={
        "id": current_user.id,
        "username" : current_user.username
    }

    return jsonify(user_data)

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
