# app
from flask import Flask
from flask_migrate import Migrate
from .routes import register_blueprints
from .extensions import db
from flask_login import LoginManager

login_manager = LoginManager()

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)
  login_manager.login_view = 'user_bp.login'

  register_blueprints(app)

  return app

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
