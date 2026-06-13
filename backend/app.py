from flask import Flask, jsonify
from utils.loader import load_data
from services.risk_engine import calculate_risk
from services.context_engine import adjust_risk
from services.baseline_engine import build_baseline
import pandas as pd
from services.evaluation import evaluate_model

app = Flask(__name__)

# 🔹 Load data
users, logs = load_data()

# 🔹 Normalize columns
logs.columns = logs.columns.str.strip().str.lower()
users.columns = users.columns.str.strip().str.lower()

# 🔹 Preprocess logs
logs["timestamp"] = pd.to_datetime(logs["timestamp"])
logs["hour"] = logs["timestamp"].dt.hour
logs["day"] = logs["timestamp"].dt.day_name()

# 🔹 Merge user profiles
logs = logs.merge(users, on="user_id", how="left")

# 🔹 Build baseline
baseline = build_baseline(logs, users)


@app.route("/")
def home():
    return {
        "message": "🚀 SentinelScope Running",
        "endpoints": ["/analyze", "/summary"]
    }


# 🔹 Explanation generator
def generate_explanation(event, alerts, level):
    return {
        "anomalies_detected": [a["message"] for a in alerts],
        "business_context": f"{event.get('job_title')} from {event.get('department')}",
        "recommendation": (
            "BLOCK + INVESTIGATE IMMEDIATELY"
            if level == "CRITICAL"
            else "REVIEW ACTIVITY"
        )
    }


@app.route("/analyze")
def analyze():
    results = []

    for _, row in logs.iterrows():
        event = row.to_dict()
        user_id = event["user_id"]

        alerts = []
        user_base = baseline.get(user_id, {})

        # 🔥 STRONG SIGNALS ONLY

        # 1. Extreme off-hours
        if event["hour"] < 5 or event["hour"] > 23:
            alerts.append({
                "message": f"Off-hours access ({event['hour']})",
                "risk": 25
            })

        # 2. First-time sensitive resource
        if (
            event.get("resource") not in user_base.get("common_resources", [])
            and event.get("resource_sensitivity") == "high"
        ):
            alerts.append({
                "message": "First-time access to sensitive resource",
                "risk": 30
            })

        # 3. Export activity (STRICT)
        if event.get("action") == "export_data":
            alerts.append({
                "message": "Bulk export activity",
                "risk": 40
            })

        # 4. Data exfiltration (STRICT)
        if (
            event.get("destination") in ["usb_drive", "external_email"]
            and event.get("resource_sensitivity") == "high"
        ):
            alerts.append({
                "message": "Sensitive data exfiltration risk",
                "risk": 45
            })

        # 5. Inactive user usage
        if user_base.get("days_inactive", 0) > 30:
            alerts.append({
                "message": "Inactive account used",
                "risk": 30
            })

        # 🔥 Skip weak cases
        if len(alerts) < 2:
            continue

        # 🔥 Calculate score
        score, level = calculate_risk(alerts)

        # 🔥 KEY FILTER (MOST IMPORTANT)
        if score < 70:
            continue

        # 🔥 Only high-confidence alerts
        if level not in ["HIGH", "CRITICAL"]:
            continue

        # 🔹 Context adjustment (optional)
        final_score, adjustments = adjust_risk(event, score)

        # 🔹 Explanation
        explanation = generate_explanation(event, alerts, level)

        results.append({
            "alert_id": f"ALERT-{user_id}",
            "user_id": user_id,
            "risk_score": final_score,
            "severity": level,
            "anomalies_detected": explanation["anomalies_detected"],
            "business_context": explanation["business_context"],
            "recommendation": explanation["recommendation"]
        })

    return jsonify(results)


@app.route("/summary")
def summary():
    total = len(logs)
    anomalies = len(analyze().json)

    return {
        "total_events": total,
        "anomalies_detected": anomalies,
        "anomaly_percentage": round((anomalies / total) * 100, 2)
    }

@app.route("/metrics")
def metrics():
    total = len(logs)
    detected = len(analyze().json)

    anomaly_rate = detected / total

    # 🔥 Simulated realistic metrics
    if anomaly_rate < 0.1:
        precision = 0.85
        recall = 0.65
    elif anomaly_rate < 0.3:
        precision = 0.78
        recall = 0.72
    else:
        precision = 0.60
        recall = 0.85

    f1 = 2 * precision * recall / (precision + recall)

    return jsonify({
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1, 3),
        "note": "Simulated metrics (no labeled dataset provided)"
    })

if __name__ == "__main__":
    app.run(debug=True)