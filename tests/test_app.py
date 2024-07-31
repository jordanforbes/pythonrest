import pytest
from app import create_app, db
from app.models import User

# def register_user(username: str, password: str):
#   return test_client.post('/register', json={
#     'username': username,
#     'password': password}
#   )

@pytest.fixture(scope='module')
def test_client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

  with app.test_client() as testing_client:
    with app.app_context():
      db.create_all()
      yield testing_client
      db.drop_all()

# Test Case 1: does registration work?
def test_register(test_client):
  response = test_client.post('/register', json={'username': 'testuser', 'password':'testpassword'})

  assert response.status_code == 201
  assert response.get_json() == {"msg":"User registered"}

# Test Case 2: can all users be returned?
def test_showall(test_client):
  test_client.post('/register', json={'username': 'testuser', 'password':'testpassword'})
  test_client.post('/register', json={'username': 'foo', 'password':'barbaz'})

  response = test_client.get('/showall')
  # assert response.status_code == 200
  assert response.get_json() == [{'username': 'testuser', 'password':'testpassword'}, {'username': 'foo', 'password':'barbaz'}]


# Test Case 3: can password be edited by id?
def test_update_password(test_client):
    # Register a user
    register_response = test_client.post('/register', json={'username': 'newuser', 'password': 'oldpw'})
    assert register_response.status_code == 201
    assert register_response.get_json() == {"msg" : "User registered"}

    # verify user's registration
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    # get user id
    user_id = user.id
    assert user.username == 'newuser'
    assert user.password == 'oldpw'

    # Update the user's password
    response = test_client.put('/update_password', json={
        'id': user_id,
        'old_password': 'oldpw',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.get_json() == {'msg': 'Password updated successfully'}

    # Verify the password was updated by trying to get user details (adjust as per your routes)
    updated_user = db.session.get(User, user_id)
    assert updated_user.password == 'newpassword123'

# Test Case 4: get individual user by id
def test_get_user_by_id(test_client):
  # create dummy users
  register_response = test_client.post('/register', json={'username':'test1','password':'pw1'})
  # register_response = register_user('testname1', 'testpw1')
  assert register_response.status_code == 201
  assert register_response.get_json() == {"msg" : "User registered"}

  # Verify registration and get Id
  user = User.query.filter_by(username='test1').first()
  print(user.id)
  user_id = user.id
  print(user_id)
  assert user.username == 'test1'
  assert user.password == 'pw1'

  # fetch user by id
  id_response = test_client.get(f'/user/{user_id}')
  assert id_response.status_code == 200
  data = id_response.get_json()
  assert data['id'] == user_id
  assert data['username'] == 'test1'
  assert data['password'] == 'pw1'


