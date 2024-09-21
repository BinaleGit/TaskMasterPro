# TaskMasterPro

TaskMasterPro is an AI-powered to-do list application that helps users prioritize and manage their tasks efficiently. By utilizing machine learning, TaskMasterPro automatically calculates task priorities based on deadlines and estimated completion time, enabling users to focus on what matters most.

## Features

- **AI-Driven Prioritization**: TaskMasterPro uses a machine learning model to predict the priority of tasks.
- **Task Categorization**: Tasks are grouped into 'Today', 'Tomorrow', 'Upcoming', and 'Past Due' categories.
- **User Authentication**: Secure login and registration system.
- **Task Management**: Add, delete, and mark tasks as done with ease.
- **Mobile Responsive**: The application is designed to work on all devices, using Tailwind CSS for styling.
  
## Directory Structure

```plaintext
TaskMasterPro/
├── auth/
│   └── routes.py               # User authentication routes
│
├── tasks/
│   └── routes.py               # Task management routes (add, update, delete)
│
├── templates/
│   ├── about.html              # About page
│   ├── index.html              # Main task view page
│   ├── login.html              # Login page
│   └── register.html           # Register page
│
├── instance/
│   └── app.db                  # SQLite database
│
├── app.py                      # Main Flask application
├── extensions.py               # Flask extensions (SQLAlchemy, Flask-Login)
├── models.py                   # SQLAlchemy database models And AI Models (User, Task)
├── requirements.txt            # Python dependencies
├── tailwind.config.js          # Tailwind CSS configuration
└── README.md                   # Project documentation
```
## Installation
 - Prerequisites
 - Python 3.x
 - Node.js and npm (for Tailwind CSS)
 - Virtual Environment (recommended)
 
 ## Setup
 1. Clone the repository:

 ```
 git clone https://github.com/YourUsername/TaskMasterPro.git
    cd TaskMasterPro
```
2. Set up a virtual environment:
 ```
 python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```
3. Install Python dependencies:
```
pip install -r requirements.txt
```
4. Install Node.js dependencies:
```
npm install
```
5. Initialize the database:
```
flask db init
flask db migrate
flask db upgrade
```
6. Run the application:
```
flask run
```
The app will be running at http://127.0.0.1:5000/.

## Optional: Compile Tailwind CSS
```
npm run build-css
```
## Usage
1. Register: Create an account to start managing tasks.
2. Login: Access your personalized task list.
3. Add Tasks: Input the task name, deadline, estimated time, and priority.
4. AI-Powered Prioritization: TaskMasterPro uses AI to calculate and display the most urgent tasks.
5. Manage Tasks: Mark tasks as done, update details, or delete tasks as necessary.
## Technologies Used
 - Flask: Python web framework for building the backend.
 - Flask-Login: User authentication.
 - Flask-SQLAlchemy: ORM for handling SQLite database.
 - Pandas and Scikit-learn: Data processing and machine learning for task prioritization.
 - Tailwind CSS: For responsive UI design.
 - Jinja2: Templating engine for HTML rendering.

 Created with ❤️ by Roee.








