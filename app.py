from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    estimated_time = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Boolean, default=False)
    in_progress = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User

# Load user for session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database tables
with app.app_context():
    db.create_all()

# Calculate time left until the deadline
def calculate_time_left(deadline):
    now = datetime.now()
    time_diff = deadline - now

    if time_diff.total_seconds() < 0:
        return "Expired"

    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

# Home route with task management
@app.route('/')
@login_required
def home():
    # Load tasks from the database for the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Group tasks based on deadlines
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    past_due = [task for task in tasks if task.deadline.date() < today]
    today_tasks = [task for task in tasks if task.deadline.date() == today]
    tomorrow_tasks = [task for task in tasks if task.deadline.date() == tomorrow]
    upcoming_tasks = [task for task in tasks if task.deadline.date() > tomorrow]

    return render_template('index.html', past_due_tasks=past_due, today_tasks=today_tasks, 
                           tomorrow_tasks=tomorrow_tasks, upcoming_tasks=upcoming_tasks)

# Add Task route
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_name = request.form['task_name']
    deadline_date = request.form['deadline']
    task_time = request.form['time']
    priority = int(request.form['priority'])
    deadline = datetime.strptime(f"{deadline_date} {task_time}:00", '%Y-%m-%d %H:%M:%S')
    estimated_time = int(request.form['estimated_time'])

    # Create a new task for the current user
    new_task = Task(task_name=task_name, priority=priority, deadline=deadline, 
                    estimated_time=estimated_time, user_id=current_user.id)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('home'))

# Mark task as done
@app.route('/mark_done/<int:task_id>', methods=['POST'])
@login_required
def mark_done(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.done = True
        db.session.commit()
    return redirect(url_for('home'))

# Mark task as in progress
@app.route('/mark_in_progress/<int:task_id>', methods=['POST'])
@login_required
def mark_in_progress(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.in_progress = True
        task.done = False
        db.session.commit()
    return redirect(url_for('home'))

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists. Try another one.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check your username and password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# User logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# About page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
