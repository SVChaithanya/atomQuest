📌 AtomQuest Goal Management System

A scalable goal tracking and performance management platform built with FastAPI and modern backend architecture principles.

🚀 Key Features
Secure JWT-based Authentication
Role-Based Access Control (RBAC)
Admin
Manager
Employee
Goal Creation, Assignment & Tracking
Quarterly Performance Updates
Goal Approval Workflow (Manager-driven)
Manager Check-ins for progress review
Active Performance Cycle Management
Goal Weightage Validation System
Team-level Performance Monitoring
🧱 Tech Stack
Backend
FastAPI (Python)
SQLAlchemy ORM
SQLite (development)
JWT Authentication
Frontend
React.js
Tailwind CSS
🔌 API Modules
🔐 Authentication
Register User
Login User
Get Current User
🎯 Goals
Create Goal
Update Goal
Fetch My Goals
👨‍💼 Manager Operations
View Team Goals
Approve / Reject Goals
Conduct Check-ins
🛠 Admin Operations
Manage Users
Manage All Goals
Create & Manage Cycles
📁 Project Structure
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
⚙️ Local Setup Instructions
1. Create Virtual Environment
python -m venv venv
2. Activate Environment

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Application
uvicorn main:app --reload

Application will be available at:

http://127.0.0.1:8000
🐳 Docker Deployment
docker-compose up --build
👨‍💻 Author

Surya Yaramati
