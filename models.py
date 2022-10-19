from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    name = db.Column(db.String(30), nullable=True)

# class room_detail(db.Model):
#     __tablename__ = 'room_detail'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     price = db.Column(db.Integer)


class User(db.Model, UserMixin):

   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String, unique=True, index=True)
   email = db.Column(db.String, unique=True, index=True)
   password = db.Column(db.String)

class Message(db.Model):

   __tablename__ = 'messages'
   id = db.Column(db.Integer, primary_key = True)
   from_ = db.Column(db.Integer, unique=False, nullable=False)
   to_ = db.Column(db.Integer, unique=False, nullable=False)
   body = db.Column(db.String)