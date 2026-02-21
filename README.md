# 🚑 Golden Hour Response – AI-Powered Emergency Healthcare System

### 🧠 Built for **ZYND Aickathon | Healthcare (Golden Hour Track)**

> **Saving lives in the most critical hour through intelligent, coordinated AI agents.**

---

## 🌟 Problem Statement

In medical emergencies, the **Golden Hour**—the first 60 minutes after trauma—is crucial.
Delays in **triage, hospital allocation, routing, and communication** often result in preventable loss of life.

### ⚠️ Current Challenges

* Manual emergency coordination
* No real-time hospital capacity awareness
* Delayed ambulance routing
* Fragmented communication systems

---

## 💡 Our Solution

**Golden Hour Response** is a **multi-agent AI healthcare coordination system** that uses **ZYND Protocol** to enable real-time collaboration between intelligent agents.

Each agent independently reasons about a critical part of the emergency response while the **Orchestrator** ensures seamless coordination.

---

## 🧠 Core Concept: Multi-Agent Intelligence

This system follows **ZYND’s “From Agents to Intelligence Networks”** philosophy.

```
Emergency Event
     ↓
🧠 Triage Agent
     ↓
🏥 Hospital Agent
     ↓
🚑 Routing Agent
     ↓
📢 Notification Agent
     ↓
🌐 Frontend (Live Updates)
```

---

## 🤖 AI Agents Overview

| Agent                  | Responsibility                                 |
| ---------------------- | ---------------------------------------------- |
| **Triage Agent**       | Classifies emergency severity using AI logic   |
| **Hospital Agent**     | Finds nearest hospital with available capacity |
| **Routing Agent**      | Calculates optimal ambulance route             |
| **Notification Agent** | Sends alerts to hospitals, responders & UI     |

Each agent works **independently** yet collaborates through **ZYND Protocol events**.

---

## ⚙️ System Architecture

```
Frontend (Vite + React)
        ↑  ↓  (REST + WebSockets)
FastAPI Backend
        ↓
🧠 Orchestrator (Event-Driven)
        ↓
🤖 AI Agents (Triage | Hospital | Routing | Notification)
        ↓
🗄️ Database (Seeded Hospital & Emergency Data)
        ↓
🔗 ZYND Protocol (Mocked for Hackathon)
```

---


## 🗄️ Database & Seed Data

To simulate real-world conditions, we include:

* Seeded hospitals with capacity & location
* Sample emergency cases
* Verification scripts

📁 Location:

```
backend/src/database/
```

---

## 🌐 API & Real-Time Communication

### REST APIs

* Emergency creation
* Hospital availability
* Agent status

### WebSockets

* Live emergency updates
* Real-time agent decisions
* Frontend notification stream

📁 Location:

```
backend/src/api/
```

---


## 🚀 How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Khushi5155/Golden-Hour-Response-Healthcare---ZYND-AICKATHON.git
cd Golden-Hour-Response-Healthcare---ZYND-AICKATHON

```

### 2️⃣ Backend Setup (JS Backend)

```bash
cd js-backend
npm init -y
npm install express mongoose bcryptjs jsonwebtoken dotenv cors

```
#### Run the backend 

```bash
node server.js

```
#### Backend URL 
```bash
http://localhost:5000
```
---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev

```


---

## 🎯 Hackathon Alignment

✔ Multi-Agent Architecture

✔ ZYND Protocol Integration

✔ Real-Time Coordination

✔ Healthcare Impact

✔ Scalable & Extensible Design

---

## 🔮 Future Enhancements

---

## 👩‍💻 Team

Built with ❤️ by **CrypticByte**
for **ZYND Aickathon – Healthcare Track**

---

> **Because every second matters in the Golden Hour.**
