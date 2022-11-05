import inspect
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
   monthly_rent = db.Column(db.Integer)
   is_bill_included = db.Column(db.Boolean)
   deposit = db.Column(db.Integer)
   start_date =  db.Column(db.DateTime)
   room_type = db.Column(db.String(30))
   duration = db.Column(db.String(100))
   is_furnished = db.Column(db.Boolean)
   gender = db.Column(db.String(30))
   is_smorkable = db.Column(db.Boolean)
   with_landload = db.Column(db.Boolean)
   postcode = db.Column(db.String(30))
   area = db.Column(db.String(30))
   closest_station = db.Column(db.String(30))
   picture_path = db.Column(db.String(100))
   created_at = db.Column(db.DateTime)
   def toDict(self):
      return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }




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