from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.User import User

user_bp = Blueprint('user_bp', __name__)

# ////////////////////////////////////
# create user
@user_bp.route('/register', methods = ['POST'])
def register():

  data = request.get_json()

  username = data.get('username')
  password = data.get('password')

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
@user_bp.route('/user/<int:user_id>', methods = ['DELETE'])
def delete_user_by_id(user_id):
  user = User.query.get(user_id)
  if not user:
    return jsonify({"msg" : "user not found"}), 404

  db.session.delete(user)
  db.session.commit()

  return jsonify({"msg" : "user deleted"}), 200
