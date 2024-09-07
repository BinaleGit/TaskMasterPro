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
model = train_model(df)

# Function to calculate the time left until the deadline
def calculate_time_left(deadline):
    now = datetime.now()
    if isinstance(deadline, str):
        deadline = pd.to_datetime(deadline, errors='coerce')  # Ensure 'deadline' is in datetime format
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

@app.route('/')
def home():
    show_done = request.args.get('show_done', 'false')  # Get the show_done param from the URL
    # Load tasks from CSV
    df = pd.read_csv('tasks.csv')

    df['deadline'] = pd.to_datetime(df['deadline'], format='%Y-%m-%d %H:%M:%S', errors='coerce')  # Convert to datetime
    
    # Calculate time left for each task
    df['time_left'] = df['deadline'].apply(calculate_time_left)

    # Ensure 'priority' is numeric
    df['priority'] = pd.to_numeric(df['priority'], errors='coerce')

    if show_done == 'false':  # Hide done tasks by default
        df = df[df['done?'] == False]

    tasks = df.to_dict(orient='records')  # Convert to list of dicts for rendering
    return render_template('index.html', tasks=tasks, show_done=show_done)


# Route to mark a task as done
@app.route('/mark_done/<task_name>', methods=['POST'])
def mark_done(task_name):
    df = pd.read_csv('tasks.csv')
    df.loc[df['task_name'] == task_name, 'done?'] = True
    df.to_csv('tasks.csv', index=False)
    return redirect(url_for('home'))

# Route to mark a task as in progress
@app.route('/mark_in_progress/<task_name>', methods=['POST'])
def mark_in_progress(task_name):
    df = pd.read_csv('tasks.csv')
    df.loc[df['task_name'] == task_name, 'in_progress'] = True
    df.loc[df['task_name'] == task_name, 'done?'] = False  # Ensure task is not marked as done
    df.to_csv('tasks.csv', index=False)
    return redirect(url_for('home'))

# Route to show done tasks
@app.route('/show_done_tasks')
def show_done_tasks():
    return redirect(url_for('home', show_done='true'))

# Route to hide done tasks
@app.route('/hide_done_tasks')
def hide_done_tasks():
    return redirect(url_for('home', show_done='false'))

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    deadline_date = request.form['deadline']
    task_time = request.form['time']  # Get specific time from the form
    priority = request.form['priority']  # Get user-defined priority
    
    # Combine the deadline date and specific time into full datetime format
    deadline = f"{deadline_date} {task_time}:00".strip()  # Format as YYYY-MM-DD HH:MM:SS
    
    done_status = False  # Default status for new tasks is "Not Done"
    in_progress_status = False  # Default for new tasks is "Not In Progress"

    # Get estimated time from the form
    estimated_time = request.form.get('estimated_time')

    # Predict AI priority using the custom priority provided by the user
    task = {
        'estimated_time': estimated_time,
        'deadline': deadline
    }

    # Use the AI model to combine AI priority and user-provided priority
    final_priority = predict_priority(task, priority, model)

    # Manually map priority into encoded form
    priority_mapping = {
        'High': 1,
        'Medium': 2,
        'Low': 3
    }
    priority_encoded = priority_mapping.get(final_priority, 3)

    # Create a new DataFrame for the new task
    new_task = pd.DataFrame({
        'task_name': [task_name],
        'priority': [final_priority],  # Use the combined priority
        'priority_encoded': [priority_encoded],  # Use the encoded priority
        'deadline': [deadline],  # Save the full deadline with date and time
        'estimated_time': [estimated_time],
        'done?': [done_status],
        'in_progress': [in_progress_status]
    })

    # Load the CSV and append the new task
    df = pd.read_csv('tasks.csv')
    df = pd.concat([df, new_task], ignore_index=True)
    df.to_csv('tasks.csv', index=False)

    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)
