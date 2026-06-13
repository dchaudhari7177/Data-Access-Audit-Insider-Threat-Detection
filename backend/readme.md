# 🚀 Data Access Audit & Insider Threat Detection System

## 📌 Overview

This project is a **Data Access Monitoring and Insider Threat Detection System** designed to detect suspicious user behavior across enterprise data systems.

It analyzes data access logs, identifies anomalies using a **rule-based + behavior-aware approach**, and generates **risk scores, alerts, and explanations** to help security teams respond quickly.

---

## 🎯 Problem Statement

Enterprises process **millions of data access events daily**, making it difficult to:

* Detect unauthorized or abnormal data access
* Differentiate between normal and suspicious behavior
* Prevent insider threats and data exfiltration
* Reduce false positives from naive alerting systems

---

## 💡 Solution

This system provides:

* 📥 **Log Ingestion** (CSV-based, extendable to APIs)
* ⚙️ **Rule-Based Detection Engine**
* 🧠 **User Behavior Baseline Modeling**
* 📊 **Risk Scoring System**
* 🧾 **Explainable Alerts**
* 📉 **False Positive Reduction via Context Awareness**

---

## 🏗️ Architecture

```
Data Logs → Rule Engine → Baseline Engine → Context Engine
          → Risk Scoring → Explanation Engine → API Output
```

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Data Processing:** Pandas, NumPy
* **Storage:** CSV (extendable to PostgreSQL/MongoDB)
* **Frontend (planned):** React + Tailwind CSS
* **Evaluation:** Scikit-learn (Precision, Recall, F1)

---

## 📂 Project Structure

```
backend/
 ├── app.py
 ├── rules/
 │    └── rules.json
 ├── services/
 │    ├── rule_engine.py
 │    ├── risk_engine.py
 │    ├── context_engine.py
 │    ├── baseline_engine.py
 │    └── explanation_engine.py
 ├── utils/
 │    └── loader.py
 ├── data/
 │    ├── user_profiles.csv
 │    ├── data_access_logs.csv
```

---

## ⚙️ Core Components

### 1. Rule Engine

* Evaluates access events using predefined JSON rules
* Detects:

  * After-hours access
  * High-volume access
  * Sensitive data access

---

### 2. Baseline Engine

* Builds **user-specific behavior profiles**
* Tracks:

  * Average access time
  * Typical data volume
  * Common data sensitivity

👉 Enables **behavior-aware anomaly detection**

---

### 3. Risk Scoring Engine

* Aggregates risk from triggered rules
* Assigns severity levels:

| Score | Level    |
| ----- | -------- |
| 0–30  | Low      |
| 30–60 | Medium   |
| 60–80 | High     |
| 80+   | Critical |

---

### 4. Context Engine

* Adjusts risk using real-world context:

  * Weekends
  * User roles (admin vs normal)
  * Known exceptions

👉 Reduces false positives significantly

---

### 5. Explanation Engine

* Generates human-readable explanations:

```
User U2 accessed sensitive data in high volume at unusual hours,
deviating from normal behavior.
```

👉 Improves interpretability for analysts

---

## 🧪 Example Output

```json
{
  "user": "U2",
  "risk_score": 90,
  "risk_level": "CRITICAL",
  "alerts": [
    {"message": "Access outside normal working hours"},
    {"message": "Unusually high data access volume"},
    {"message": "Access to highly sensitive data"}
  ],
  "explanation": "User accessed large volume of sensitive data at abnormal hours."
}
```

---

## 📊 Evaluation Metrics

The system is evaluated using labeled datasets:

* **Precision** (>75%) → reduce false alerts
* **Recall** (>70%) → detect real threats
* **F1 Score** (>0.72) → overall performance

---

## 🚀 How to Run

### 1. Install dependencies

```
pip install flask pandas numpy
```

### 2. Run backend

```
python app.py
```

### 3. Open in browser

```
http://127.0.0.1:5000/analyze
```

---

## 🔥 Advanced Features (Implemented)

* ✅ Rule-based anomaly detection
* ✅ User behavior baseline modeling
* ✅ Risk scoring system
* ✅ Context-aware adjustments
* ✅ Explainable alerts

---

## 🚀 Future Enhancements (MAKE IT ADVANCED)

### 🧠 Intelligence Upgrades

* Add statistical anomaly detection (Z-score, IQR)
* Hybrid ML model (Isolation Forest)
* Role-based dynamic thresholds

---

### ⚡ Real-Time Processing

* Kafka-based log ingestion
* Streaming detection pipeline
* Real-time alerts using WebSockets

---

### 📊 Advanced Dashboard

* Interactive React dashboard
* Risk heatmaps
* User activity timelines
* Drill-down investigation view

---

### 🔐 Security Enhancements

* Role-based access control (RBAC)
* Audit trail storage
* Integration with DLP systems

---

### 🤖 AI Enhancements

* LLM-based alert explanations
* Natural language query system
* Automated incident reports

---

### 🧪 Evaluation Improvements

* Confusion matrix visualization
* Threshold tuning
* False positive tracking

---

### ☁️ Scalability Design

To handle **1M+ events/day**:

* Use **Kafka** for ingestion
* Use **Spark Streaming** for processing
* Use **distributed storage** (BigQuery, Cassandra)
* Partition data by user/time

---

## 🏆 Key Highlights

* Combines **rule-based + behavioral analysis**
* Focuses on **explainability and usability**
* Designed for **real-world enterprise scenarios**
* Extensible to **ML and real-time systems**

---

## 📌 Conclusion

This system demonstrates how a **simple rule-based approach can be enhanced with behavioral context and explainability** to build a scalable and practical insider threat detection solution.

---

## 👨‍💻 Author

Dipak Chaudhari
BTech CSE | Full Stack Developer
Focused on building scalable and intelligent systems

---
