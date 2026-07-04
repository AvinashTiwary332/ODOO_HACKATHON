from datetime import date, datetime
from functools import wraps
from flask import abort, flash, redirect, session, url_for
from models import Employee, Notification, User, db


def current_user():
    user_id = session.get("user_id")
    return User.query.get(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                return redirect(url_for("auth.login"))
            if user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def parse_date(value, field_name="date"):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError(f"Enter a valid {field_name}.")


def notify(user_id, title, message):
    db.session.add(Notification(user_id=user_id, title=title, message=message))


def seed_demo_data():
    if User.query.first():
        return
    admin = User(name="Aarav Admin", email="admin@hrms.test", role="Admin")
    admin.set_password("Admin@123")
    hr = User(name="Hira HR", email="hr@hrms.test", role="HR Officer")
    hr.set_password("Hr@12345")
    employee_user = User(name="Esha Patel", email="employee@hrms.test", role="Employee")
    employee_user.set_password("Employee@123")
    db.session.add_all([admin, hr, employee_user])
    db.session.flush()
    employees = [
        Employee(user_id=admin.id, employee_id="EMP-1000", department="Leadership", designation="System Admin", joining_date=date(2022, 1, 5), phone="9000000001", address="Ahmedabad", salary=120000),
        Employee(user_id=hr.id, employee_id="EMP-1001", department="People Ops", designation="HR Officer", joining_date=date(2022, 6, 12), phone="9000000002", address="Mumbai", salary=85000),
        Employee(user_id=employee_user.id, employee_id="EMP-1002", department="Engineering", designation="Frontend Engineer", joining_date=date(2023, 3, 20), phone="9000000003", address="Bengaluru", salary=72000),
    ]
    db.session.add_all(employees)
    db.session.commit()
