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


#postgres://afya_check_user:3ZuYV9VQPrrd1LmPrXmJORgs7tWVybOX@dpg-cmgdn0gl5elc73fs5330-a.oregon-postgres.render.com/afya_check
#postgres://akilicheck_database_user:Ju5HWhDLsJqnSGnhkjasC1ezjHq3edzf@dpg-cops4tdjm4es73aakde0-a/akilicheck_database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "secret_key_from_env"

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt with the app

from app import views
