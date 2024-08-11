class Config:
  SECRET_KEY = 'foobar'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = 'bazbaz'
