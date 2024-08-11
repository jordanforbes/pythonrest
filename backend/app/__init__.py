# app
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from .routes import register_blueprints
from .extensions import db, login_manager
# from flask_login import LoginManager
from .models import User
from flask_jwt_extended import JWTManager
# import jwt


migrate = Migrate()
jwt=JWTManager()

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config.from_object('app.config.Config')



  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)
  jwt.init_app(app)

  login_manager.login_view = 'auth_bp.login'

# load the user by ID
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  @app.route('/')
  def index():
    return app

  register_blueprints(app)
  return app
