import pytest
from app import create_app
from app.models.User import User
from app.models.Post import Post
from app.extensions import db

@pytest.fixture(scope = "module")
def test_client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

  with app.test_client() as testing_client:
    with app.app_context():
      db.create_all()
      yield testing_client
      db.drop_all()

# //////////////////////////////////////////////////////////////////
# Test Case 1: does Posting work?
def test_create_post(test_client):
  # register user
  response = test_client.post('/api/register', json={'username': 'testuser', 'password':'testpassword'})
  assert response.status_code == 201

  # retrieve user to get user_id
  user = User.query.filter_by(username="testuser").first()
  user_id = user.id

  # create post
  response = test_client.post('/api/posts', json={'title':'testtitle','content':'testcontent','user_id': user_id})
  assert response.status_code == 201
  assert response.get_json({"msg": "Post created successfully"})

# //////////////////////////////////////////////////////////////////
# Test Case 2: can you retrieve all posts?
def test_get_posts(test_client):
  response = test_client.get('/api/posts')
  assert response.status_code == 200
  data = response.get_json()
  assert isinstance(data, list)

# //////////////////////////////////////////////////////////////////
# Test Case 3: can you retrieve one post by id
def test_get_post_by_id(test_client):
  post = Post.query.first()
  post_id = post.id

  response = test_client.get(f'/api/posts/{post_id}')
  assert response.status_code == 200
  data = response.get_json()
  assert data['id'] == post_id


# //////////////////////////////////////////////////////////////////
# Test Case 4: can you delete one post by id
def test_delete_post_by_id(test_client):
  post = Post.query.first()
  post_id = post.id

  response = test_client.delete(f'/api/posts/{post_id}')
  assert response.status_code == 200
  assert response.get_json({"msg":"post successfully deleted"})

  post = Post.query.get(post_id)
  assert post is None
