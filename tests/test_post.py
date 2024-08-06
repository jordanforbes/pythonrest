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
# def test_get_all_posts(test_client):
