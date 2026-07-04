# Human Resource Management System

A complete Flask ODOO_HACKATHON for hackathon demos with role-based login, employee management, attendance, leave approvals, payroll, profile uploads, dashboards, charts, and responsive Bootstrap UI.

## Requirements

- Python 3.10+
- MySQL 8+ for production-style setup
- Optional: SQLite is used automatically when `DATABASE_URL` is not set, so the app runs immediately for local demos.

## Installation

```bash
cd ODOO_HACKATHON
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Demo accounts created automatically for SQLite:

- Admin: `admin@hrms.test` / `Admin@123`
- HR Officer: `hr@hrms.test` / `Hr@12345`
- Employee: `employee@hrms.test` / `Employee@123`

## MySQL Setup

```bash
mysql -u root -p < database/schema.sql
```

Set the connection string before running:

```bash
set DATABASE_URL=mysql+pymysql://root:password@localhost/hrms_db
python app.py
```

The Flask app uses SQLAlchemy ORM and will create mapped tables if they do not exist. `database/schema.sql` is included for direct MySQL import with primary keys, foreign keys, timestamps, and indexes.

## Features

- Registration, login, logout, forgot password screen, password hashing, and session-based access control
- Admin and HR dashboards with cards, charts, leave statistics, payroll summary, and recent activity
- Employee directory with search, edit, delete, and profile view
- Attendance check-in/check-out, working hour calculation, admin approval, and history
- Leave application with paid, sick, casual, and unpaid leave types plus admin approve/reject comments
- Payroll generation for admin/HR and read-only salary slips for employees
- Employee profile with editable phone/address and profile picture upload
- 403, 404, and 500 error pages with friendly messages

## Folder Structure

```text
ODOO_HACKATHON/
  app.py
  config.py
  requirements.txt
  README.md
  database/
  models/
  routes/
  templates/
  static/
  utils/
  instance/
```