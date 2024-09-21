import os
from flask import Flask
from extensions import db, login_manager  # Import db and login_manager from extensions
from auth.routes import auth_bp  # Import auth blueprint
from tasks.routes import tasks_bp  # Import tasks blueprint

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Use your actual secret key
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# Initialize extensions with the app

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

# Define user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    # Ensure the app context is active
    with app.app_context():
        db.create_all()  # Create all tables (this will create tables based on your models)
    app.run(debug=True)