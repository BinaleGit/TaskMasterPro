import logging
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db



# User model for authentication

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    estimated_time = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Boolean, default=False)
    in_progress = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Machine Learning Functions for Priority Prediction


logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

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

    # Check the number of samples and avoid train-test split if too few samples
    if len(X_scaled) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    else:
        X_train, y_train = X_scaled, y

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, scaler

def predict_priority(task, user_priority, model, scaler):
    now = datetime.now()
    task['time_until_deadline'] = (pd.Timestamp(task['deadline']) - now).total_seconds() / 3600
    task['estimated_time'] = pd.to_numeric(task['estimated_time'], errors='coerce')
    task_features = [[task['estimated_time'], task['time_until_deadline']]]
    task_features_scaled = scaler.transform(task_features)

    # Predict AI priority
    ai_priority_encoded = model.predict(task_features_scaled)[0]

    # Log the AI prediction and user priority
    logging.info(f"AI Predicted Priority: {ai_priority_encoded}, User Priority: {user_priority}")

    # Calculate the final priority
    final_priority = (float(ai_priority_encoded) + float(user_priority)) / 2

    # Log the final priority
    logging.info(f"Final Calculated Priority: {final_priority}")

    return final_priority