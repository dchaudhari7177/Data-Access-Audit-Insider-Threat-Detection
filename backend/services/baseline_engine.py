import pandas as pd


def build_baseline(logs: pd.DataFrame, users: pd.DataFrame):
    """
    Baseline adapted for dataset WITHOUT rowcount
    """

    baseline = {}

    if logs.empty or users.empty:
        return baseline

    # 🔹 Normalize columns
    logs.columns = logs.columns.str.strip().str.lower()
    users.columns = users.columns.str.strip().str.lower()

    # 🔹 Ensure datetime
    logs["timestamp"] = pd.to_datetime(logs["timestamp"])
    logs["hour"] = logs["timestamp"].dt.hour

    grouped = logs.groupby("user_id")

    for user_id, group in grouped:

        group = group.dropna(subset=["hour"])

        if group.empty:
            continue

        # 🔹 Time behavior
        avg_hour = group["hour"].mean()
        std_hour = group["hour"].std() if len(group) > 1 else 1

        # 🔹 Most accessed resources
        common_resources = list(group["resource"].value_counts().head(3).index)

        # 🔹 Most common actions
        common_actions = list(group["action"].value_counts().head(2).index)

        # 🔹 Most common sensitivity
        try:
            common_sensitivity = group["resource_sensitivity"].mode()[0]
        except:
            common_sensitivity = "unknown"

        # 🔹 Fetch user profile
        user_profile = users[users["user_id"] == user_id]

        if not user_profile.empty:
            user_profile = user_profile.iloc[0]

            baseline[user_id] = {
                "avg_hour": float(avg_hour),
                "std_hour": float(std_hour),
                "common_resources": common_resources,
                "common_actions": common_actions,
                "common_sensitivity": common_sensitivity,
                "department": user_profile.get("department", "unknown"),
                "job_title": user_profile.get("job_title", "unknown"),
                "privilege_level": user_profile.get("privilege_level", "unknown"),
                "days_inactive": user_profile.get("days_inactive", 0),
                "is_active": user_profile.get("is_active", True)
            }

        else:
            baseline[user_id] = {
                "avg_hour": float(avg_hour),
                "std_hour": float(std_hour),
                "common_resources": common_resources,
                "common_actions": common_actions,
                "common_sensitivity": common_sensitivity,
                "department": "unknown",
                "job_title": "unknown",
                "privilege_level": "unknown",
                "days_inactive": 0,
                "is_active": True
            }

    return baseline