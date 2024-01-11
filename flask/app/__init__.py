from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt  # Import Bcrypt

app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///afya_check.db"
app.config["SQLALCHEMY_DATABASE_URI"] = '''postgres://lajtmhynnlgztg:bedc78ff8cf870eba8f875debf44c60d54b30c9f409737c2032c4608dc3349a1@ec2-35-169-9-79.compute-1.amazonaws.com:5432/dasgr4ki63k3je
'''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "secret_key_from_env"

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt with the app

from app import views
