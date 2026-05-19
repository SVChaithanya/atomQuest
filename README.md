Use this. Your old README was weak and generic. This version actually looks like a hackathon submission instead of a classroom CRUD project.

````md
# AtomQuest Goal Management System

A modern enterprise performance management platform built using FastAPI, PostgreSQL, and Docker.

The system enables organizations to manage employee goals, quarterly progress tracking, manager approvals, and performance cycles through a secure role-based workflow.

---

# Features

## Authentication & Security
- JWT Authentication
- Access & Refresh Tokens
- Password Hashing using Bcrypt
- Role-Based Access Control (RBAC)

---

# User Roles

## Admin
- Create performance cycles
- View all users
- Monitor all goals
- Track organization-wide progress

## Manager
- View team goals
- Approve or reject employee goals
- Add quarterly check-ins
- Monitor employee performance

## Employee
- Create goals
- Update goals before approval
- Submit quarterly progress updates
- Track goal completion percentage

---

# Core Functionalities

## Goal Management
- Maximum 8 goals per cycle
- Weightage validation (max 100%)
- Goal approval workflow
- Goal locking after approval

## Quarterly Tracking
- Quarterly performance updates
- Planned vs actual achievement tracking
- Automatic completion percentage calculation
- Progress monitoring dashboard support

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
````

---

# API Endpoints

## Authentication

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/api/auth/register` |
| POST   | `/api/auth/login`    |

---

## User

| Method | Endpoint  |
| ------ | --------- |
| GET    | `/api/me` |

---

## Goals

| Method | Endpoint                        |
| ------ | ------------------------------- |
| POST   | `/api/goals`                    |
| GET    | `/api/goals/my-goals`           |
| PUT    | `/api/goals/{goal_id}`          |
| PUT    | `/api/goals/{goal_id}/approval` |

---

## Quarterly Updates

| Method | Endpoint                                |
| ------ | --------------------------------------- |
| POST   | `/api/goals/{goal_id}/quarterly-update` |

---

## Manager

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | `/api/manager/team-goals`   |
| POST   | `/api/checkins/{update_id}` |

---

## Admin

| Method | Endpoint               |
| ------ | ---------------------- |
| POST   | `/api/cycles`          |
| GET    | `/api/cycles`          |
| GET    | `/api/admin/users`     |
| GET    | `/api/admin/all-goals` |

---

# Database Design

## Main Tables

* USERS
* GOALS
* CYCLES
* QUARTERLY_UPDATES
* MANAGER_CHECKINS

---

# Setup Instructions

## Clone Repository

```bash
git clone <your_repo_link>
cd atomQuest
```

---

# Run with Docker

## Build and Start Containers

```bash
docker-compose up --build
```

---

# Backend Server

Backend runs on:

```bash
http://localhost:8000
```

Swagger API Docs:

```bash
http://localhost:8000/docs
```

---

# Environment Variables

```env
DATABASE_URL=postgresql://postgres:password@db:5432/atomquest
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Sample Workflow

## Employee

1. Register/Login
2. Create goals
3. Submit quarterly updates

## Manager

1. View team goals
2. Approve or reject goals
3. Add manager check-ins

## Admin

1. Create performance cycles
2. Monitor all users and goals

---

# Future Improvements

* Email Notifications
* OTP Authentication
* Analytics Dashboard
* Redis Caching
* AI-Based Performance Insights
* Frontend Deployment
* Kubernetes Deployment

---

# Team

Developed for AtomQuest Hackathon 2026.

---

# License

This project is developed for educational and hackathon purposes.

````

This is now:
- cleaner
- recruiter readable
- hackathon level
- professional enough for judges

Do NOT leave placeholders like:
```bash
git clone <your_repo_link>
````

Replace them before submission or it looks unfinished.
