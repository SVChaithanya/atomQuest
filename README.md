# AtomQuest Goal Management System

A modern enterprise performance and goal tracking platform built using FastAPI, PostgreSQL, and Docker.

The platform enables organizations to manage employee goals, track quarterly progress, handle manager approvals, and monitor performance cycles through a secure role-based workflow.

---

# Live Deployment

## Production API

http://13.206.196.40:8000

## Swagger API Documentation

http://13.206.196.40:8000/docs

---

# Features

## Authentication & Security
- JWT Authentication
- Access & Refresh Tokens
- Password Hashing using Bcrypt
- Secure Login System
- Role-Based Access Control (RBAC)

---

# User Roles

## Admin
- Create and manage performance cycles
- View all users
- Monitor organization-wide goals
- Track employee progress

## Manager
- View team goals
- Approve or reject employee goals
- Add quarterly manager check-ins
- Monitor employee performance

## Employee
- Create personal goals
- Update goals before approval
- Submit quarterly updates
- Track progress percentage

---

# Core Functionalities

## Goal Management
- Maximum 8 goals per cycle
- Weightage validation (total must not exceed 100%)
- Goal approval workflow
- Goal locking after approval

## Quarterly Progress Tracking
- Quarterly updates submission
- Planned vs actual achievement tracking
- Automatic completion percentage calculation
- Progress monitoring support

## Performance Cycles
- Active cycle management
- Cycle-based goal tracking
- Admin-controlled cycle activation

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic
- JWT Authentication

## DevOps
- Docker
- Docker Compose

---

# Project Structure

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
├── .gitignore
└── README.md
```

---

# API Endpoints

# Authentication

| Method | Endpoint |
|---|---|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |

---

# User

| Method | Endpoint |
|---|---|
| GET | `/api/me` |

---

# Goals

| Method | Endpoint |
|---|---|
| POST | `/api/goals` |
| GET | `/api/goals/my-goals` |
| PUT | `/api/goals/{goal_id}` |
| PUT | `/api/goals/{goal_id}/approval` |

---

# Quarterly Updates

| Method | Endpoint |
|---|---|
| POST | `/api/goals/{goal_id}/quarterly-update` |

---

# Manager

| Method | Endpoint |
|---|---|
| GET | `/api/manager/team-goals` |
| POST | `/api/checkins/{update_id}` |

---

# Admin

| Method | Endpoint |
|---|---|
| POST | `/api/cycles` |
| GET | `/api/cycles` |
| GET | `/api/admin/users` |
| GET | `/api/admin/all-goals` |

---

# Database Tables

- USERS
- GOALS
- CYCLES
- QUARTERLY_UPDATES
- MANAGER_CHECKINS

---

# Setup Instructions

# Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/atomQuest.git

cd atomQuest
```

---

# Create Virtual Environment

```bash
python -m venv venv
```

---

# Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

## Linux / Mac

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Backend Server

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# Run with Docker

## Build and Start Containers

```bash
docker-compose up --build
```

---

# Docker Services

## Backend
- FastAPI Application
- Port: 8000

## Database
- PostgreSQL 15
- Port: 5432

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/atomquest
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Sample Workflow

# Employee Workflow

1. Register/Login
2. Create goals
3. Update goals
4. Submit quarterly progress updates

---

# Manager Workflow

1. Login
2. View team goals
3. Approve or reject goals
4. Add manager check-ins

---

# Admin Workflow

1. Create performance cycles
2. View all users
3. Monitor all goals

---

# Validation Rules

- Maximum 8 goals per employee
- Total goal weightage cannot exceed 100%
- Approved goals become locked
- One quarterly update per quarter

---

# Future Improvements

- OTP Authentication
- Email Notifications
- Analytics Dashboard
- Redis Caching
- AI-Based Performance Insights
- Frontend Deployment
- Kubernetes Deployment

---

# Team

Developed for AtomQuest Hackathon 2026.

---

# License

This project is developed for educational and hackathon purposes.
