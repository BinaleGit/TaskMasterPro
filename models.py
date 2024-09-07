from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd

# Train the model to predict task priority
def train_model(df):
    # Convert the 'deadline' column to datetime format
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    
    # Drop rows with NaT in 'deadline'
    df = df.dropna(subset=['deadline'])
    
    # Convert 'deadline' to numeric timestamps
    df['deadline_numeric'] = df['deadline'].apply(lambda x: x.timestamp() if pd.notnull(x) else None)
    
    # Manual mapping of priority values (1 is the highest priority)
    priority_mapping = {
        'High': 1,
        'Medium': 2,
        'Low': 3
    }

    # Apply the mapping to the 'priority' column
    df['priority_encoded'] = df['priority'].map(priority_mapping)
    
    # Ensure 'estimated_time' is numeric
    df['estimated_time'] = pd.to_numeric(df['estimated_time'], errors='coerce')

    # Check for missing values in 'priority_encoded'
    if df['priority_encoded'].isnull().any():
        print("Warning: Missing values found in 'priority_encoded'. Removing rows with missing priorities.")
        df = df.dropna(subset=['priority_encoded'])  # Remove rows with NaN in 'priority_encoded'

    # Prepare features (X) and target (y)
    X = df[['estimated_time', 'deadline_numeric']]  # Features must be numeric
    y = df['priority_encoded']  # Encoded priority as the target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model



# Function to predict task priority using both AI model and user input
def predict_priority(task, user_priority, model):
    # Convert the deadline to numeric format (timestamp)
    task['deadline'] = pd.Timestamp(task['deadline']).timestamp()

    # Ensure estimated time is numeric
    task['estimated_time'] = pd.to_numeric(task['estimated_time'], errors='coerce')

    # Prepare features for prediction
    task_features = [[task['estimated_time'], task['deadline']]]

    # AI model predicts the priority (numeric)
    ai_priority_encoded = model.predict(task_features)[0]

    # Debug output
    print("Task Features:", task_features)
    print("AI Priority Encoded:", ai_priority_encoded)
    print("User Priority:", user_priority)

    # Combine AI-predicted priority with the user-provided custom priority
    final_priority = (float(ai_priority_encoded) + float(user_priority)) / 2

    print("Final Priority:", final_priority)

    # Map back to a priority label if needed
    return final_priority

