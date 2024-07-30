from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return jsonify(message='Hello world')

# create user
@main.route('/register', methods = ['POST'])
def register():
  data = request.get_json()

  username = data.get('username')
  password = data.get('password')

  if not username or not password:
    return jsonify({"msg": "Missing username or password"}), 400

  if User.query.filter_by(username=username).first():
    return jsonify({"msg":"Username already exists"}),400

  user = User(username=username, password=password)
  db.session.add(user)
  db.session.commit()

  return jsonify({"msg":"User registered"}), 201

# get all users
@main.route('/showall', methods = ['GET'])
def showall():
  users = User.query.all()
  users_list =  [{"username": user.username, "password": user.password} for user in users]
  print(f'users list: {users_list}')
  return jsonify(users_list), 200

# edit user's password
@main.route('/update_password', methods=['PUT'])
def update_password():
  data = request.get_json()
  username = data.get('username')
  old_password = data.get('old_password')
  new_password = data.get('new_password')

  # validate input
  if not username or old_password or not new_password:
    return jsonify({"msg": "Missing username, old password, or new password"}), 400

  # find user by username
  user = User.query.filter_by(username=username).first()

  if not user:
    return jsonify({"msg": "User not found"}), 404

  # check if old password is correct
  if user.password != old_password:
    return jsonify({"msg": "incorrect old password"}), 400

  user.password = new_password
  db.session.commit()

  return jsonify({"msg": "Password updated successfully"}), 200
