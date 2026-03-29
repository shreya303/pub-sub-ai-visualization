# 🚀 AI-Powered Event Analytics Pipeline

A real-time event processing and analytics system built using **GCP Pub/Sub, BigQuery, Python, and Streamlit**, enhanced with an **AI-powered query interface**.

---

## 🧠 Overview

This project simulates a production-grade **event-driven data pipeline**:

- Events are generated in real-time using Python
- Published to **GCP Pub/Sub**
- Processed asynchronously by a subscriber
- Stored in **BigQuery**
- Queried and visualized using a **Streamlit dashboard**
- Supports **natural language querying (AI-powered / fallback logic)**

---

## 🏗️ Architecture

# 🚀 AI-Powered Event Analytics Pipeline

A real-time event processing and analytics system built using **GCP Pub/Sub, BigQuery, Python, and Streamlit**, enhanced with an **AI-powered query interface**.

---

## 🧠 Overview

This project simulates a production-grade **event-driven data pipeline**:

- Events are generated in real-time using Python
- Published to **GCP Pub/Sub**
- Processed asynchronously by a subscriber
- Stored in **BigQuery**
- Queried and visualized using a **Streamlit dashboard**
- Supports **natural language querying (AI-powered / fallback logic)**

---

## 🏗️ Architecture

Producer (Python)

↓

GCP Pub/Sub (Topic)

↓

Subscriber (Python Worker)

↓

Processing Logic

↓

BigQuery (Storage)

↓

Streamlit App (Visualization + AI Queries)


## 📁 Project Structure
PUB-SUB/

pub-sub/

│ ├── constants.py

│ ├── producer.py

│ ├── subscriber.py


visualization/

│ ├── app.py

README.md


## ⚙️ Tech Stack

- **Python**
- **Google Cloud Pub/Sub**
- **Google BigQuery**
- **Streamlit**
- **OpenAI API (optional)**
- **Pandas**

---

## 🚀 Features

### 🔹 Real-Time Event Pipeline
- Simulates user activity (payments, logins, transfers)
- Publishes events in batches to Pub/Sub

### 🔹 Fault-Tolerant Processing
- Subscriber consumes messages asynchronously
- Retry + Dead Letter Queue support
- Handles failures gracefully

### 🔹 BigQuery Storage
- Structured schema for analytics
- Partitioned by timestamp for performance
- Raw payload stored for flexibility

### 🔹 AI-Powered Querying
- Convert natural language → SQL
- Fallback rule-based system (no API required)

### 🔹 Interactive Dashboard
- Query results displayed in tables
- Auto-generated charts
- Insight summaries

---

## 📊 Sample Queries

- "Show total number of events by event type"
- "Top 5 users with most flagged transactions"
- "Number of flagged vs non-flagged events"
- "Average transaction amount per user"

---

## 🧪 Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/pub-sub-event-analytics.git
cd pub-sub-event-analytics
```

Built with ❤️ by Shreya