from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Creating the app
app = Flask(__name__)

#Setting database parameters
app.config['SECRET_KEY']='117811a0828d154166b134acc6a16e5327f93d5ae080d3c2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my_flask_app.db')

#Creating the database
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


from my_flask_app import routes