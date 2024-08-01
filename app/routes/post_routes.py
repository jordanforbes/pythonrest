from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.Post import Post
from ..models.User import User

post_bp = Blueprint('post_bp', __name__)

# //////////////////////////////////
# create post
@post_bp.route('/posts', methods=['POST'])
def create_post():
  data = request.get_json()

  title = data.get('title')
  content = data.get('content')
  user_id = data.get('user_id')

  if not title or not content or not user_id:
    return jsonify({"msg": "invalid title or content or user_id"}), 400

  user = User.query.get(user_id)
  if not user:
    return jsonify({"msg": "user not found"}), 404

  post = Post(title=title, content=content, user_id=user_id)
  db.session.add(post)
  db.session.commit()

  return jsonify({"msg": "Post created successfully"}), 201


# //////////////////////////////////
# get all posts
@post_bp.get('/posts', methods= ['GET'])
def get_posts():
  posts = Post.query.all()
  posts_list = [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
  return jsonify(posts_list), 200
