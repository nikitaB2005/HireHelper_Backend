# HireHelper - Backend API

This is the Django-based backend API for HireHelper, providing authentication, task management, and notification services.

**Live Deployment:**
- **API Base URL**: [https://hirehelper-backend-desq.onrender.com/api/](https://hirehelper-backend-desq.onrender.com/api/)
- **Admin Panel**: [https://hirehelper-backend-desq.onrender.com/admin/](https://hirehelper-backend-desq.onrender.com/admin/)

## Tech Stack
- **Framework**: Django & Django Rest Framework (DRF)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: SimpleJWT
- **Deployment**: Render / Gunicorn

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your credentials (see `.env.example`).
6. Run migrations: `python manage.py migrate`
7. Start server: `python manage.py runserver`
