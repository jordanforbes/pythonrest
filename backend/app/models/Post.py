from datetime import datetime
from ..extensions import db

class Post(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(255), nullable = False)
   content = db.Column(db.Text, nullable = False)
   created_at = db.Column(db.DateTime, default=datetime.now)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

   user = db.relationship('User', backref=db.backref('posts', lazy=True))

   def __repr__(self):
      return f'<Post {self.title}>'
