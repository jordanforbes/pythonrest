from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return jsonify(message='Hello world')

@main.route('/register', methods = ['POST'])
def register():
  print('its hitting register in routes')
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

  return jsonify({"msg":"User registered"}), 400
