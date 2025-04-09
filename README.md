# Nexus-AI: Multi-Agent Attendance Management System

Nexus-AI is an AI-powered attendance management system developed as a senior thesis project at The College of Wooster. The system integrates facial recognition, autonomous agents, and natural language processing to modernize and streamline attendance tracking in educational settings. It features dashboards for students, professors, and administrators and is designed to ensure ethical, controlled, and intelligent attendance monitoring.

---

## What the Project Does

Nexus-AI is a multi-agent system that manages student attendance using facial recognition and autonomous agents that respond to user interaction. When a student logs in, their identity is verified using OpenCV and Euclidean distance-based facial recognition. A chatbot interface allows students to query their attendance status, and professors can manually generate attendance reports.

All system interactions—such as data retrieval, alerts, and predictions—are handled by specialized agents. Reports and alerts are only triggered when requested by the user, preserving control and data privacy.

---

## Why the Project Is Useful

This system automates a typically time-consuming and manual process while enhancing transparency for both professors and students. By integrating AI-powered agents and user interaction controls, it demonstrates how modern technologies can solve real-world problems in education. It avoids full automation, ensuring privacy and accountability through manual triggers.

Key benefits include:

- Reduced administrative workload for instructors
- Real-time access to attendance data for students
- Early warning of potential absenteeism trends
- Scalable, modular architecture suitable for future expansion

---
## System Features

### Admin Dashboard
- Assign professors and students to classrooms
- Manage user roles and classrooms
- Manually generate and export attendance reports

### Professor Dashboard
- Start and stop facial recognition attendance sessions
- View student lists, attendance records, and submitted justifications
- Send replies directly to student messages

### Student Dashboard
- View personal attendance activity
- Submit absence justifications
- Chat with an AI agent for assistance
- Receive alerts when absenteeism crosses a threshold
---

## Tech Stack

| Layer         | Technology                            |
|---------------|----------------------------------------|
| **Frontend**  | HTML, CSS, JavaScript, Bootstrap, GSAP |
| **Backend**   | Python (Flask), SQLite                 |
| **AI/NLP**    | GPT-3.5 (via OpenAI API), Scikit-learn |
| **Facial Rec**| OpenCV, Euclidean distance matching    |

## Agents Overview

The project’s core intelligence is implemented using a modular multi-agent system. Each agent has a specific function and is invoked only when needed through the main Flask backend.

### Core Agents and Their Roles

- `alert_agent.py`: Sends alerts to professors when a student’s absences exceed a specified threshold.
- `coordinator.py`: Central controller that routes user input to the correct agent based on the detected intent.
- `insights_agent.py`: Generates summaries and graphs of attendance patterns using statistical analysis and GPT.
- `prediction_agent.py`: Predicts the likelihood of future absences based on historical attendance data.
- `query_agent.py`: Classifies user input, identifies relevant keywords (such as course names), and passes the query to the correct module.
- `retrieval_agent.py`: Retrieves current absence counts for a given student based on course logs.

The `AgentCoordinator` acts as the communication hub between the dashboard interface and the intelligent agents.

---
## Project Documentation
### 1. Clone the repository
### 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # (On Windows: venv\Scripts\activate)
### 3. Install Requirements
pip install -r requirements.txt

### 4. Run the app
python app.py

### 5. Open in browser
http://127.0.0.1:5000/



