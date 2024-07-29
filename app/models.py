from .extensions import db, bcrypt

class User(db.Model):
  id = db.Column(db.String(150), unique = True, nullable = False)
  username = db.Column(db.String(150), unique = True, nullable = False)
  password = db.Column(db.String(150), nullable = False)

  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

  def check_password(self, password):
    return bcrypt.check_password_hash(self.password,password)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(100), nullable = False)
  description = db.Column(db.Text, nullable = False)
  status = db.Column(db.String(20), nullable = False)
  priority = db.Column(db.String(20), nullable = False)
  due_date = db.Column(db.DateTime, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
