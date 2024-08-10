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
      db.session.remove()
      db.drop_all()

# Helper function to register and login a user
def register_and_login(test_client, username, password):
    # Register the user
    response = test_client.post('/api/register', json={'username': username, 'password': password})
    assert response.status_code == 201

    # Login the user
    response = test_client.post('/api/login', json={'username': username, 'password': password})
    assert response.status_code == 200

    # Extract the token from the login response
    token = response.get_json()['token']
    return token

# //////////////////////////////////////////////////////////////////
# Test Case 1: does Posting work after login?
def test_create_post(test_client):
  # register and login user to get token
  token = register_and_login(test_client, "testuser","testpassword")


  # # retrieve user to get user_id
  user = User.query.filter_by(username="testuser").first()
  assert user is not None
  user_id = user.id

  # create post
  response = test_client.post('/api/posts',
                              json={'title':'testtitle','content':'testcontent', 'user_id':user_id},
                              headers={'Authorization':f'Bearer {token}'})
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
