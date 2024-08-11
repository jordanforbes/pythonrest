import pytest
from app import create_app
from app.extensions import db
from app.models.User import User

@pytest.fixture(scope="module")
def test_client():
  app = create_app()
  app.config["TESTING"] = True
  app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///:memory:'
  # create flask app test client
  with app.test_client() as testing_client:
    with app.app_context():
      # initialize database
      db.create_all()
      yield testing_client
      # drop database after test is complete
      db.drop_all()

@pytest.fixture(scope="module")
def init_database():
  # initialize database with a user for login tests
  user = User(username="testuser")
  user.set_password("testpassword")
  db.session.add(user)
  db.session.commit()
  yield db
  # reset everything after tests
  db.session.close_all()
  db.drop_all()

# Test Case 1: user can login
def test_login_and_create_post(test_client, init_database):
  # login the user through POST request to login endpoint
  login_response = test_client.post('/api/login', json={"username":"testuser","password":"testpassword"})
  # assert login is successful
  assert login_response.status_code == 200
  # assert login_response.get_json() == {"msg": "Login successful"}

# Test Case 2: logged in user can post
# def test_login_and_create_post(test_client, init_database):
#   # login the user through POST request to login endpoint
#   login_response = test_client.post('/api/login', json={"username":"testuser","password":"testpassword"})
#   # assert login is successful
#   assert login_response.status_code == 200
#   assert login_response.get_json() == {"msg": "Login successful"}

#   # retrieve user from db to get id
#   user = User.query.filter_by(username='testuser').first()
#   user_id = user.id

#   # create post as logged in user

