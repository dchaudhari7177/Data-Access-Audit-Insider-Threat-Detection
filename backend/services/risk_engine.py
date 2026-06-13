def calculate_risk(alerts):
    total = sum(a["risk"] for a in alerts)

    # 🔥 stricter thresholds
    if total >= 90:
        level = "CRITICAL"
    elif total >= 70:
        level = "HIGH"
    elif total >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return total, level