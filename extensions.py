from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
