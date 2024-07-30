import pytest
from app import create_app, db
from app.models import User

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
  assert response.status_code == 200
  assert response.get_json() == [{'username': 'testuser', 'password':'testpassword'}, {'username': 'foo', 'password':'barbaz'}]

