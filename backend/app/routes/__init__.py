from flask import Blueprint, jsonify, send_from_directory

from .user_routes import user_bp
from .post_routes import post_bp
from .auth_routes import auth_bp

main = Blueprint('main', __name__)

@main.route('/api')
def home():
  return jsonify({'msg':'Welcome to the API!'}), 200
  # return send_from_directory('static','index.html')

# register all blueprints
def register_blueprints(app):
  app.register_blueprint(user_bp, url_prefix="/api")
  app.register_blueprint(post_bp, url_prefix="/api")
  app.register_blueprint(auth_bp, url_prefix="/api")
  app.register_blueprint(main)
