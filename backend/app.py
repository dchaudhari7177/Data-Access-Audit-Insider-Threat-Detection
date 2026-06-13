from flask import Flask, jsonify
from utils.loader import load_data
from services.rule_engine import RuleEngine
from services.risk_engine import calculate_risk
from services.context_engine import adjust_risk
from services.baseline_engine import build_baseline

app = Flask(__name__)

# 🔹 Load data
users, logs = load_data()

# 🔹 Initialize engines
rule_engine = RuleEngine("rules/rules.json")
baseline = build_baseline(logs)


# 🔹 Home Route
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 Data Access Monitoring System Running",
        "endpoints": {
            "analyze": "/analyze",
            "summary": "/summary"
        }
    })


# 🔹 Explanation Engine
def generate_explanation(event, alerts, score, level, adjustments):
    reasons = [a["message"] for a in alerts]

    adjustment_text = ", ".join([a["reason"] for a in adjustments]) if adjustments else "No contextual adjustments"

    return {
        "summary": f"{level} risk detected for user {event.get('user_id')}",
        "details": f"User triggered {len(alerts)} anomalies: " + ", ".join(reasons),
        "context": adjustment_text,
        "recommendation": "Investigate user activity, verify access legitimacy, and take action if required."
    }


# 🔹 Analyze Route
@app.route("/analyze")
def analyze():
    results = []

    for _, row in logs.iterrows():
        event = row.to_dict()
        user_id = event.get("user_id")

        # 🔸 Step 1: Rule-based alerts
        alerts = rule_engine.evaluate(event)

        # 🔸 Step 2: Baseline comparison
        user_base = baseline.get(user_id, {})

        if user_base:
            avg_hour = user_base.get("avg_hour", 0)
            std_hour = user_base.get("std_hour", 1)
            max_volume = user_base.get("max_volume", 1)

            # Time anomaly (statistical)
            if abs(event["hour"] - avg_hour) > max(2 * std_hour, 3):
                alerts.append({
                    "rule_id": "baseline_time",
                    "risk": 25,
                    "message": "Unusual access time compared to user behavior"
                })

            # Volume anomaly
            if event["volume"] > max_volume * 2:
                alerts.append({
                    "rule_id": "baseline_volume",
                    "risk": 35,
                    "message": "Abnormal data volume compared to user history"
                })

        # 🔸 Step 3: Process only if anomalies exist
        if alerts:
            # Risk scoring
            base_score, level = calculate_risk(alerts)

            # Context adjustment
            final_score, adjustments = adjust_risk(event, base_score)

            # Recalculate level after adjustment
            if final_score >= 80:
                final_level = "CRITICAL"
            elif final_score >= 60:
                final_level = "HIGH"
            elif final_score >= 30:
                final_level = "MEDIUM"
            else:
                final_level = "LOW"

            # Explanation
            explanation = generate_explanation(
                event, alerts, final_score, final_level, adjustments
            )

            results.append({
                "user": user_id,
                "risk_score": final_score,
                "risk_level": final_level,
                "alerts": alerts,
                "adjustments": adjustments,
                "explanation": explanation,
                "baseline": user_base
            })

    return jsonify(results)


# 🔹 Summary Route
@app.route("/summary")
def summary():
    total_events = len(logs)
    anomalies = 0

    for _, row in logs.iterrows():
        event = row.to_dict()
        alerts = rule_engine.evaluate(event)
        if alerts:
            anomalies += 1

    return jsonify({
        "total_events": total_events,
        "anomalies_detected": anomalies,
        "anomaly_percentage": round((anomalies / total_events) * 100, 2)
    })


# 🔹 Run App
if __name__ == "__main__":
    app.run(debug=True)