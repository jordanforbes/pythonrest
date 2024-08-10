from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models.User import User
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user_bp', __name__)

# ////////////////////////////////////
# create user
@user_bp.route('/register', methods = ['POST'])
def register():
  print('/register route')

  data = request.get_json()

  username = data.get('username')
  password = data.get('password')
  print(username)

  if not username or not password:
    return jsonify({"msg": "Missing username or password"}), 400

  if User.query.filter_by(username=username).first():
    return jsonify({"msg":"Username already exists"}),400

  user = User(username=username)
  user.set_password(password)
  db.session.add(user)
  db.session.commit()

  return jsonify({"msg":"User registered"}), 201

# ////////////////////////////////////
# login user
# @user_bp.route('/login', methods=['POST'])
# def login():
#   data = request.get_json()
#   username = data.get('username')
#   password = data.get('password')

#   user = User.query.filter_by(username=username).first()
#   if user and user.check_password(password):
#     login_user(user)
#     # token = create_access_token(identity=user.id)
#     # return jsonify(token=token), 200
#     return jsonify({"token": "fake-jwt-token"}), 200  # Replace with actual token generation

#   return jsonify({"msg": "invalid username or password"}), 401

# @user_bp.route('/logout', methods=['POST'])
# @login_required # must be logged in to logout of course
# def logout():
#   logout_user()
#   return jsonify({"msg":"user logged out"}), 200


# ////////////////////////////////////
# get all users
@user_bp.route('/users', methods = ['GET'])
def showall():
  users = User.query.all()
  users_list =  [{"username": user.username} for user in users]
  print(f'users list: {users_list}')
  return jsonify(users_list), 200

# ////////////////////////////////////
# get individual user by id
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
  user = db.session.get(User, user_id)
  print('hello')
  print(user)

  if not user:
    return jsonify({"msg":"user not found"}), 404

  return jsonify({
    "id": user.id,
    "username": user.username,
  }), 200

# ////////////////////////////////////
# edit user's password by id
@user_bp.route('/update_password', methods=['PUT'])
def update_password():
  data = request.get_json()

  user_id = data.get('id')
  old_password = data.get('old_password')
  new_password = data.get('new_password')

  # validate input
  if not user_id or not old_password or not new_password:
    print('missing username, old password, or new password')
    return jsonify({"msg": "Missing username, old password, or new password"}), 400

  # find user by username
  user = User.query.filter_by(id=user_id).first()

  if not user:
    return jsonify({"msg": "User not found"}), 404

  if not user.check_password(old_password):
    return jsonify({'msg':'incorrect old password'}), 404

  # update user's password
  user.set_password(new_password)
  db.session.commit()

  return jsonify({"msg": "Password updated successfully"}), 200

# ////////////////////////////////////
# delete a user by id
@user_bp.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user_by_id(user_id):
  user = User.query.get(user_id)
  if not user:
    return jsonify({"msg" : "user not found"}), 404

  db.session.delete(user)
  db.session.commit()

  return jsonify({"msg" : "user deleted"}), 200

