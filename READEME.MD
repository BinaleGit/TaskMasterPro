# TaskMasterPro

TaskMasterPro is an AI-powered task management application designed to help you efficiently manage and prioritize your tasks. Utilizing Flask for the backend and Tailwind CSS for the frontend, TaskMasterPro provides a seamless experience for task tracking and management.

## Features

- **AI-Powered Prioritization**: Uses machine learning to predict and set task priorities based on deadlines and user input.
- **Task Tracking**: Add, update, and track tasks with deadlines and estimated completion times.
- **Priority-Based Color Coding**: Visualize task urgency with color-coded priorities (High, Medium, Low).
- **Interactive UI**: Built with Tailwind CSS for a modern and responsive user interface.
- **Mark Tasks as Done**: Easily mark tasks as completed or in progress.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/BinaleGit/TaskMasterPro.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd TaskMasterPro
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

5. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

## Configuration

- **CSV File**: Ensure you have a `tasks.csv` file in the project directory with appropriate columns (e.g., task_name, priority, deadline, estimated_time).
- **Model Training**: The model is trained on the task data when the application starts. Make sure your dataset is up-to-date.

## Usage

- **Add Tasks**: Use the "Add a Task" form to input new tasks with deadlines, priorities, and estimated time.
- **View Tasks**: Tasks are displayed with priority-based color coding and time left until the deadline.
- **Manage Tasks**: Mark tasks as done or in progress with the provided buttons.

## Contributing

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature/YourFeature`).
3. **Make your changes**.
4. **Commit your changes** (`git commit -am 'Add new feature'`).
5. **Push to the branch** (`git push origin feature/YourFeature`).
6. **Create a new Pull Request**.


## Acknowledgements

- **Flask**: Web framework for Python.
- **Tailwind CSS**: Utility-first CSS framework.
- **Pandas**: Data analysis library for Python.
- **Scikit-learn**: Machine learning library for Python.
- **Numpy**: Numerical computing library for Python.
