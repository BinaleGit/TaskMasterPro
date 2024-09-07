import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime

# Train the model to predict task priority
def train_model(df):
    # Convert the 'deadline' column to datetime format
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')

    # Drop rows with NaT in 'deadline'
    df = df.dropna(subset=['deadline'])

    # Calculate the time left in days from now to the deadline
    now = datetime.now()
    df['time_until_deadline'] = df['deadline'].apply(lambda x: (x - now).total_seconds() / 3600)  # Hours until deadline

    # Ensure 'estimated_time' is numeric
    df['estimated_time'] = pd.to_numeric(df['estimated_time'], errors='coerce')

    # Drop rows with missing values in 'time_until_deadline' or 'estimated_time'
    df = df.dropna(subset=['time_until_deadline', 'estimated_time'])

    # Check if there is any data left
    if df.empty:
        raise ValueError("No data available for training after cleaning.")

    # Prepare features (X) and target (y)
    X = df[['estimated_time', 'time_until_deadline']]
    y = df['priority_encoded']  # Assuming this column is already in the DataFrame

    # Apply scaling to features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, scaler


# Function to predict task priority using both AI model and user input
def predict_priority(task, user_priority, model, scaler):
    # Convert the deadline to numeric format (hours until deadline)
    now = datetime.now()
    task['time_until_deadline'] = (pd.Timestamp(task['deadline']) - now).total_seconds() / 3600

    # Ensure estimated time is numeric
    task['estimated_time'] = pd.to_numeric(task['estimated_time'], errors='coerce')

    # Prepare features for prediction
    task_features = [[task['estimated_time'], task['time_until_deadline']]]

    # Scale the features
    task_features_scaled = scaler.transform(task_features)

    # AI model predicts the priority (numeric)
    ai_priority_encoded = model.predict(task_features_scaled)[0]

    # Debug output
    print("Task Features (scaled):", task_features_scaled)
    print("AI Priority Encoded:", ai_priority_encoded)
    print("User Priority:", user_priority)

    # Combine AI-predicted priority with the user-provided custom priority
    final_priority = (float(ai_priority_encoded) + float(user_priority)) / 2

    print("Final Priority:", final_priority)

    return final_priority
