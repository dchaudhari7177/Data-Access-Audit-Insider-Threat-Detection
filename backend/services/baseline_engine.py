import pandas as pd


def build_baseline(logs: pd.DataFrame):
    """
    Builds baseline behavior for each user.
    Returns a dictionary:
    {
        user_id: {
            avg_hour,
            std_hour,
            avg_volume,
            max_volume,
            common_sensitivity,
            total_events
        }
    }
    """

    baseline = {}

    if logs.empty:
        return baseline

    # Group by user
    grouped = logs.groupby("user_id")

    for user_id, group in grouped:

        # Handle missing values safely
        group = group.dropna(subset=["hour", "volume"])

        if group.empty:
            continue

        # Compute statistics
        avg_hour = group["hour"].mean()
        std_hour = group["hour"].std() if len(group) > 1 else 0

        avg_volume = group["volume"].mean()
        max_volume = group["volume"].max()

        # Most frequent sensitivity level
        try:
            common_sensitivity = group["sensitivity"].mode()[0]
        except:
            common_sensitivity = "unknown"

        # Save baseline
        baseline[user_id] = {
            "avg_hour": float(avg_hour),
            "std_hour": float(std_hour),
            "avg_volume": float(avg_volume),
            "max_volume": float(max_volume),
            "common_sensitivity": common_sensitivity,
            "total_events": int(len(group))
        }

    return baseline