
### Data Access Audit & Insider Threat Detection System

---

## 🚀 Overview

SentinelScope is a lightweight insider threat detection system designed to monitor enterprise data access patterns and identify suspicious activities.

The system analyzes access logs, builds behavioral baselines for users, and detects anomalies using rule-based logic combined with contextual signals. It prioritizes high-precision detection to reduce false positives and provides explainable alerts for investigation.

---

## ⚙️ Features

* 📥 Log ingestion from CSV files
* 🧠 Behavioral baseline per user
* 🚨 Rule-based anomaly detection
* 📊 Risk scoring with severity levels
* 🧾 Explainable alerts with recommendations
* 📊 Flask-based dashboard for visualization

---

## 🛠️ Tech Stack

* Python (Flask)
* Pandas
* HTML (Flask templates)

---

## ▶️ How to Run

### 1. Clone Repository

```bash
git clone https://github.com/dchaudhari7177/Data-Access-Audit-Insider-Threat-Detection
cd Data-Access-Audit-Insider-Threat-Detection/backend
```

---

### 2. Install Dependencies

```bash
pip install flask pandas flask-cors
```

---

### 3. Run Backend

```bash
python app.py
```

---

### 4. Open in Browser

* API:

```
http://127.0.0.1:5000/analyze
```

* Dashboard:

```
http://127.0.0.1:5000/dashboard
```
* Metrices:

```
http://127.0.0.1:5000/metrics
```

---

## 📊 Evaluation Metrics

* Precision: **0.85**
* Recall: **0.65**
* F1 Score: **0.737**

*(Metrics are simulated due to absence of labeled dataset)*

---

## 👤 Author

Chaudhari Dipak Rajendra
PES1UG24CS804
[dipakchaudhari171@gmail.com](mailto:dipakchaudhari171@gmail.com)
