from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt  # Import Bcrypt
import os

app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///afya_check.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")


 #postgres://akilicheck_user:jWwFujRV6IzRbKCO7NWSE9gaPXN772pM@dpg-cos8tl20si5c739r6av0-a.oregon-postgres.render.com/akilicheck
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "secret_key_from_env"

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt with the app

from app import views
