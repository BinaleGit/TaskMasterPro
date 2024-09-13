from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from models import train_model, predict_priority
from datetime import datetime

app = Flask(__name__)

# Load tasks from the CSV
def load_tasks():
    df = pd.read_csv('tasks.csv')
    return df

# Train the model when the application starts
df = load_tasks()
model, scaler = train_model(df)

# Function to calculate the time left until the deadline
def calculate_time_left(deadline):
    now = datetime.now()
    if isinstance(deadline, str):
        deadline = pd.to_datetime(deadline, errors='coerce')
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

from datetime import timedelta

@app.route('/')
def home():
    # Load tasks from CSV
    df = pd.read_csv('tasks.csv')
    
    # Convert deadlines to datetime and calculate time left
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    df['time_left'] = df['deadline'].apply(calculate_time_left)
    
    # Ensure 'priority' is numeric
    df['priority'] = pd.to_numeric(df['priority'], errors='coerce')
    
    # Get current date and next day for filtering tasks
    today = pd.Timestamp.now().normalize()
    tomorrow = today + timedelta(days=1)

    # Group tasks based on deadlines
    past_due = df[df['deadline'] < today]
    today_tasks = df[(df['deadline'] >= today) & (df['deadline'] < tomorrow)]
    tomorrow_tasks = df[(df['deadline'] >= tomorrow) & (df['deadline'] < tomorrow + timedelta(days=1))]
    upcoming_tasks = df[df['deadline'] >= tomorrow + timedelta(days=1)]
    
    # Convert to dict for rendering
    past_due_tasks = past_due.to_dict(orient='records')
    today_tasks = today_tasks.to_dict(orient='records')
    tomorrow_tasks = tomorrow_tasks.to_dict(orient='records')
    upcoming_tasks = upcoming_tasks.to_dict(orient='records')
    
    return render_template('index.html', past_due_tasks=past_due_tasks, today_tasks=today_tasks, 
                           tomorrow_tasks=tomorrow_tasks, upcoming_tasks=upcoming_tasks)



@app.route('/mark_done/<task_name>', methods=['POST'])
def mark_done(task_name):
    df = pd.read_csv('tasks.csv')
    df.loc[df['task_name'] == task_name, 'done?'] = True
    df.to_csv('tasks.csv', index=False)
    return redirect(url_for('home'))

@app.route('/mark_in_progress/<task_name>', methods=['POST'])
def mark_in_progress(task_name):
    df = pd.read_csv('tasks.csv')
    df.loc[df['task_name'] == task_name, 'in_progress'] = True
    df.loc[df['task_name'] == task_name, 'done?'] = False
    df.to_csv('tasks.csv', index=False)
    return redirect(url_for('home'))

@app.route('/show_done_tasks')
def show_done_tasks():
    return redirect(url_for('home', show_done='true'))

@app.route('/hide_done_tasks')
def hide_done_tasks():
    return redirect(url_for('home', show_done='false'))

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    deadline_date = request.form['deadline']
    task_time = request.form['time']
    priority = request.form['priority']
    deadline = f"{deadline_date} {task_time}:00".strip()
    done_status = False
    in_progress_status = False
    estimated_time = request.form.get('estimated_time')

    task = {
        'estimated_time': estimated_time,
        'deadline': deadline
    }

    final_priority = predict_priority(task, priority, model, scaler)

    new_task = pd.DataFrame({
        'task_name': [task_name],
        'priority': [final_priority],
        'priority_encoded': [final_priority],
        'deadline': [deadline],
        'estimated_time': [estimated_time],
        'done?': [done_status],
        'in_progress': [in_progress_status]
    })

    df = pd.read_csv('tasks.csv')
    df = pd.concat([df, new_task], ignore_index=True)
    df.to_csv('tasks.csv', index=False)

    return redirect(url_for('home'))

@app.route('/retrain', methods=['POST'])
def retrain_model():
    df = load_tasks()
    global model, scaler
    model, scaler = train_model(df)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
