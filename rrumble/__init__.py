from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '45d24dccce68f56a9c81270a0c91bfa4ad141d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sanzen.db'
db = SQLAlchemy(app)
guard = Bcrypt(app)
osyrus = LoginManager(app)

from rrumble import routes
