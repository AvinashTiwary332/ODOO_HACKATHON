import re
from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import Employee, User, db
from utils.helper import current_user, parse_date


auth_bp = Blueprint("auth", __name__)


def valid_password(password):
    return len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"\d", password)


@auth_bp.route("/")
def index():
    user = current_user()
    if user:
        return redirect(url_for("admin.dashboard" if user.role in ["Admin", "HR Officer"] else "employee.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email", "").lower().strip()).first()
        if user and user.is_active and user.check_password(request.form.get("password", "")):
            session.clear()
            session["user_id"] = user.id
            session["role"] = user.role
            flash(f"Welcome back, {user.name}.", "success")
            return redirect(url_for("admin.dashboard" if user.role in ["Admin", "HR Officer"] else "employee.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").lower().strip()
            employee_id = request.form.get("employee_id", "").upper().strip()
            if User.query.filter_by(email=email).first():
                raise ValueError("Email already exists.")
            if Employee.query.filter_by(employee_id=employee_id).first():
                raise ValueError("Employee ID already exists.")
            if not valid_password(request.form.get("password", "")):
                raise ValueError("Password must be 8+ characters with an uppercase letter and number.")
            user = User(name=request.form["name"].strip(), email=email, role=request.form.get("role", "Employee"))
            user.set_password(request.form["password"])
            db.session.add(user)
            db.session.flush()
            employee = Employee(
                user_id=user.id,
                employee_id=employee_id,
                department=request.form["department"].strip(),
                designation=request.form["designation"].strip(),
                joining_date=parse_date(request.form.get("joining_date")) if request.form.get("joining_date") else date.today(),
                phone=request.form.get("phone"),
                address=request.form.get("address"),
                salary=float(request.form.get("salary") or 0),
            )
            db.session.add(employee)
            db.session.commit()
            flash("Registration complete. Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as exc:
            db.session.rollback()
            flash(str(exc), "danger")
    return render_template("register.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        flash("If that email exists, a reset link would be sent by the configured mail service.", "info")
        return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
