# app
from flask import Flask
from flask_migrate import Migrate
from .routes import register_blueprints
from .extensions import db

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)

  register_blueprints(app)

  return app
