def adjust_risk(event, base_score):
    score = base_score
    adjustments = []

    user_role = event.get("role")
    day = event.get("day")
    sensitivity = event.get("sensitivity")
    volume = event.get("volume")

    if day in ["Saturday", "Sunday"]:
        score -= 10
        adjustments.append({"reason": "Weekend activity", "impact": -10})

    if user_role == "admin":
        score -= 5
        adjustments.append({"reason": "Admin role", "impact": -5})

    if sensitivity == "low":
        score -= 10
        adjustments.append({"reason": "Low sensitivity data", "impact": -10})

    if volume and volume > 50000:
        score += 20
        adjustments.append({"reason": "Extremely high volume", "impact": +20})

    score = max(score, 0)

    return score, adjustments