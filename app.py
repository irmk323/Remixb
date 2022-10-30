
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

from flask_migrate import Migrate
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app.login'

Migrate(app, db)

from views import bp
app.register_blueprint(bp)



    