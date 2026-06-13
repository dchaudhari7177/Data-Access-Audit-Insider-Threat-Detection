def calculate_risk(alerts):
    total = sum(a["risk"] for a in alerts)

    if total >= 80:
        level = "CRITICAL"
    elif total >= 60:
        level = "HIGH"
    elif total >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return total, level