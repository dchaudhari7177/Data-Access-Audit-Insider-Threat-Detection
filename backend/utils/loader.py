import pandas as pd
import os

def load_data():
    if not os.path.exists("data/user_profiles.csv"):
        raise FileNotFoundError("user_profiles.csv not found")

    if not os.path.exists("data/data_access_logs.csv"):
        raise FileNotFoundError("data_access_logs.csv not found")

    users = pd.read_csv("data/user_profiles.csv")
    logs = pd.read_csv("data/data_access_logs.csv")

    if users.empty:
        raise ValueError("user_profiles.csv is empty")

    if logs.empty:
        raise ValueError("data_access_logs.csv is empty")

    logs['timestamp'] = pd.to_datetime(logs['timestamp'])
    logs['hour'] = logs['timestamp'].dt.hour

    return users, logs