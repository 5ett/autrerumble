from rrumble import db, osyrus
from datetime import datetime
from flask_login import UserMixin

@osyrus.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    email= db.Column(db.String, unique=True, nullable=False)
    post = db.Column(db.String, nullable=False, default='not updated')
    expertise = db.Column(db.String, nullable=False, default='not updated')
    xpduration = db.Column(db.Integer, nullable=False, default='not updated')
    password = db.Column(db.String(200), unique=True, nullable=False)
    prof_photo = db.Column(db.String(50), nullable=False, default='def.jpg')
    
    def __repr__(self):
        return f"User({self.id}, '{self.name}', '{self.email}', '{self.prof_photo}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String, unique=True, nullable=False)
    guest_email= db.Column(db.String, unique=True)
    guest_tel = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    guest_msg = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.guest_name}', '{self.guest_email}', '{self.subject}', {self.date})"

