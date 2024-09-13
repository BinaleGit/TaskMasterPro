import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime

def train_model(df):
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    df = df.dropna(subset=['deadline'])
    now = datetime.now()
    df['time_until_deadline'] = df['deadline'].apply(lambda x: (x - now).total_seconds() / 3600)
    df['estimated_time'] = pd.to_numeric(df['estimated_time'], errors='coerce')
    df = df.dropna(subset=['time_until_deadline', 'estimated_time'])

    if df.empty:
        raise ValueError("No data available for training after cleaning.")

    X = df[['estimated_time', 'time_until_deadline']]
    y = df['priority_encoded']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, scaler

def predict_priority(task, user_priority, model, scaler):
    now = datetime.now()
    task['time_until_deadline'] = (pd.Timestamp(task['deadline']) - now).total_seconds() / 3600
    task['estimated_time'] = pd.to_numeric(task['estimated_time'], errors='coerce')
    task_features = [[task['estimated_time'], task['time_until_deadline']]]
    task_features_scaled = scaler.transform(task_features)
    ai_priority_encoded = model.predict(task_features_scaled)[0]
    final_priority = (float(ai_priority_encoded) + float(user_priority)) / 2
    return final_priority
