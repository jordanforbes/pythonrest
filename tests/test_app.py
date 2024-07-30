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

def test_register(test_client):
  # print(f"testclient: {test_client}")
  response = test_client.post('/register', json={'username': 'testuser', 'password':'testpassword'})
  # print(f"response: {response}")
  # print(f"status code: {response.status_code}")
  # print(f"get_json: {response.get_json()}")
  assert response.status_code == 201
  assert response.get_json() == {"msg":"User registered"}

