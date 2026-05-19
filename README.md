# AtomQuest Goal Management System

A modern performance and goal tracking platform built using FastAPI.

## Features

- JWT Authentication
- Role Based Access
  - Admin
  - Manager
  - Employee
- Goal Creation & Tracking
- Quarterly Progress Updates
- Goal Approval Workflow
- Manager Check-ins
- Active Performance Cycles
- Weightage Validation
- Team Goal Monitoring

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

### Frontend
- React.js
- Tailwind CSS

---

## API Modules

### Authentication
- Register
- Login
- Current User

### Goals
- Create Goal
- Update Goal
- My Goals

### Manager
- Team Goals
- Approve / Reject Goals
- Manager Check-ins

### Admin
- All Users
- All Goals
- Create Cycles

---

## Project Structure

```bash
atomQuest/
│
├── main.py
├── router.py
├── models.py
├── schema.py
├── auth.py
├── db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Run Locally

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Run Server

```bash
uvicorn main:app --reload
```

Server runs on:

```bash
http://127.0.0.1:8000
```

---

## Docker Run

```bash
docker-compose up --build
```

---

## Author

Surya Yaramati