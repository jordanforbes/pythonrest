# app
from flask import Flask
from flask_migrate import Migrate
from .routes import main_bp
from .extensions import db

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)

  from .routes import register_blueprints
  register_blueprints(app)

  # Import models to register them with SQLAlchemy
  with app.app_context():
    from .models import User, Post
    db.create_all()

  return app
