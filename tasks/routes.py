from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import pandas as pd
from extensions import db
from models import Task, train_model, predict_priority
from datetime import datetime, timedelta

tasks_bp = Blueprint('tasks', __name__)

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models import Task
from datetime import datetime, timedelta

# Define the blueprint
tasks_bp = Blueprint('tasks', __name__)

# Home route
@tasks_bp.route('/')
@login_required
def home():
    show_past_due = request.args.get('show_past_due', 'false') == 'true'
    
    # Fetch tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    # Filter tasks into categories
    past_due = [task for task in tasks if task.deadline.date() < today]
    today_tasks = [task for task in tasks if task.deadline.date() == today and not task.done]
    tomorrow_tasks = [task for task in tasks if task.deadline.date() == tomorrow and not task.done]
    upcoming_tasks = [task for task in tasks if task.deadline.date() > tomorrow and not task.done]

    return render_template('index.html', 
                           past_due_tasks=past_due if show_past_due else None, 
                           today_tasks=today_tasks, 
                           tomorrow_tasks=tomorrow_tasks, 
                           upcoming_tasks=upcoming_tasks, 
                           show_past_due=show_past_due)

@tasks_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_name = request.form['task_name']
    deadline_date = request.form['deadline']
    task_time = request.form['time']
    user_priority = int(request.form['priority'])  # User-provided priority
    deadline = datetime.strptime(f"{deadline_date} {task_time}:00", '%Y-%m-%d %H:%M:%S')
    estimated_time = int(request.form['estimated_time'])

    # Query the existing tasks to train the model
    with db.session.no_autoflush:
        tasks = Task.query.all()

    # Convert the tasks into a list of dictionaries, then into a pandas DataFrame
    task_dicts = [{'deadline': task.deadline, 'estimated_time': task.estimated_time, 'priority_encoded': task.priority} for task in tasks]
    df = pd.DataFrame(task_dicts)  # Convert list of dicts to a pandas DataFrame
    
    if not df.empty:  # Train the model only if there is existing data
        model, scaler = train_model(df)

        # Prepare the new task data for priority prediction
        task_data = {
            'deadline': deadline,
            'estimated_time': estimated_time
        }

        # Use the AI model to predict the task's priority
        final_priority = predict_priority(task_data, user_priority, model, scaler)
    else:
        final_priority = user_priority  # If no tasks exist, use the user's priority

    # Create the new task with AI-calculated priority
    new_task = Task(task_name=task_name, priority=final_priority, deadline=deadline,
                    estimated_time=estimated_time, user_id=current_user.id)
    
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('tasks.home'))

@tasks_bp.route('/mark_done/<int:task_id>', methods=['POST'])
@login_required
def mark_done(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)  # Delete the task from the database
        db.session.commit()
    return redirect(url_for('tasks.home'))

@tasks_bp.route('/mark_in_progress/<int:task_id>', methods=['POST'])
@login_required
def mark_in_progress(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.in_progress = True
        task.done = False
        db.session.commit()
    return redirect(url_for('tasks.home'))

@tasks_bp.route('/about')
def about():
    return render_template('about.html')

